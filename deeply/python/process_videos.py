# This code is for processing frames for CAFFEE
# It creates a dir structure under ../data/

import csv
from collections import defaultdict as dd
import subprocess as sp
import os as os
FFMPEG_BIN = 'avconv'

def read_csv_file(filename):
  naughty_dict = dd(list)
  with open(filename, 'rb') as csvfile:
    csr_reader = csv.reader(csvfile, delimiter=',')
    for row in csr_reader:       #path, start, stop
      naughty_dict[row[2].replace(' ','_').replace("'", '')].append((row[0], int(row[3]), int(row[4])))
  return naughty_dict

def open_video(filename):
  command = [ FFMPEG_BIN,  
            'i', filename,
            '']
  pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

def s_to_ffmpeg_ss(seconds):
  m, s = divmod(seconds, 60)
  h, m = divmod(m, 60)
  return str(h)+':'+str(m)+':'+str(s)

if __name__ == '__main__':
  naughty_dict = read_csv_file('../data/label.csv')
  # barf out a dir structure 4 gr8 nast
  if not os.path.exists('../data/video_frames/'):
    os.mkdir('../data/video_frames')
  for key in naughty_dict.keys():
    naughty_path = os.path.join('../data/video_frames/',key)
    if not os.path.exists(naughty_path):    
      os.mkdir(naughty_path)

  # main loop, checks for split frames, otherwise uses ffmpeg/avconv to split
  for key in naughty_dict.keys():
    for clip in naughty_dict[key]:
      print clip
      filename = os.path.basename(clip[0])
      (start, stop) = clip[1:]
      action_out_path = os.path.join('../data/video_frames/', key,str(start)+'_'+str(stop)+'.jpg')
      action_vid_path = clip[0]
      print action_out_path, action_vid_path
