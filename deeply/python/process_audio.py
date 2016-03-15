from __future__ import print_function
import sys
from optparse import OptionParser
import subprocess

import scipy.io.wavfile as wav
from tqdm import tqdm
import librosa

from process_videos import s_to_ffmpeg_ss, FFMPEG_BIN, read_csv_file

def _extract_sound(filename, output_file, start, stop):
    command_cut = [ FFMPEG_BIN,
                    '-i',  filename,
                    '-ss', s_to_ffmpeg_ss(start),
                    '-t', s_to_ffmpeg_ss(stop-start),
                    '-vn',
                    '-y', # overwrite dat shit
                    '-f', 'wav',
                    '-loglevel', '0', # stfu
                    output_file]
    subprocess.call(command_cut)

def make_mfcc_features(naughty_dict, categories=['Blowjob', 'Deep_Throat', 'Facial']):
    for category in categories:
        sys.stderr.write('processing category %s...\n' % category)
        for clip, start, stop in tqdm(naughty_dict[category]):
            tmppath = '/tmp/hot.wav'
            _extract_sound(clip, tmppath, start, stop)
            rate, sig = wav.read(tmppath)
            mfcc_features = mfcc(sig, rate)
            for fv in mfcc_features:
                print('%s,%s' % (','.join(map(str, fv)), category))

# librosa functions that:
# * take y, sr
# * return 1895 samples for /tmp/hot.wav
feature_extractors = [
    librosa.feature.chroma_stft, # 12
    librosa.feature.mfcc, # 20
    librosa.feature.chroma_cqt, # 12
    librosa.feature.spectral_centroid, # 1
    librosa.feature.spectral_bandwidth, # 1
    librosa.feature.spectral_contrast, # 7
    librosa.feature.spectral_rolloff, # 1
    librosa.feature.poly_features, # 2
    librosa.feature.tonnetz, # 6
    librosa.feature.zero_crossing_rate, # 1
]

def audio_features(naughty_dict, categories=['Blowjob', 'Deep_Throat', 'Facial']):
    for category in categories:
        sys.stderr.write('processing category %s...\n' % category)
        for clip, start, stop in tqdm(naughty_dict[category]):
            tmppath = '/tmp/hot.wav'
            _extract_sound(clip, tmppath, start, stop)
            y, sr = librosa.load('/tmp/hot.wav')
            features = []
            for fe in feature_extractors:
                features.append(fe(y, sr))
                if fe == librosa.feature.mfcc:
                    mfcc = features[-1]
                    features.append(librosa.feature.delta(mfcc)) # 20
                    features.append(librosa.feature.delta(mfcc, order=2)) # 20

            for i in range(features[0].shape[1]):
                for fv in features:
                    print('%s' % ','.join(map(str, fv[:, i])), end=',')
                print(category)

def main():
    """main function for standalone usage"""
    usage = "usage: %prog [options] csv"
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--categories', default=['Blowjob', 'Deep_Throat', 'Facial'],
                      action='append')

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return 2

    # do stuff
    audio_features(read_csv_file(args[0]), categories=options.categories)

if __name__ == '__main__':
    sys.exit(main())
