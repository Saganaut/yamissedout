import sys
from optparse import OptionParser
import subprocess

import scipy.io.wavfile as wav
from features import mfcc
from tqdm import tqdm

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
    make_mfcc_features(read_csv_file(args[0]), categories=options.categories)

if __name__ == '__main__':
    sys.exit(main())
