# This code is for processing frames for CAFFEE
# It creates a dir structure under ../data/

import csv
from collections import defaultdict as dd
import subprocess as sp
import os as os
FFMPEG_BIN = 'avconv'

def read_csv_file(filename):
  naughty_dict = dd(list)
  videos = set()
  with open(filename, 'rb') as csvfile:
    csr_reader = csv.reader(csvfile, delimiter=',')
    for row in csr_reader:       #path, start, stop
      naughty_dict[row[2].replace(' ','_').replace("'", '')].append((row[0], int(row[3]), int(row[4])))
      videos.add(row[0])
  return naughty_dict, videos

def open_video(filename):
  command = [ FFMPEG_BIN,  
            'i', filename,
            '']
  pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

def s_to_ffmpeg_ss(seconds):
  m, s = divmod(seconds, 60)
  h, m = divmod(m, 60)
  return str(h)+':'+str(m)+':'+str(s)

def resize_video_strip_sound(filename, output_file, height, width):
  print output_file
  command = [ FFMPEG_BIN, 
              'i', filename,
              's', str(height)+'x'+str(width),
              '-an',
              '-c:v',
              'copy',  output_file
            ]
  sp.call(command)

def resize_all_videos(videos, output_file_path, height, width):
  new_path = '../data/small_videos_'+str(height)+'x'+str(width)
  if not os.path.exists(new_path):    
      os.mkdir(new_path)
  for vid in videos:
    print '~~~~Processing: '+ vid.replace('_', ' ')
    resize_video_strip_sound(vid, os.path.join(new_path, os.path.basename(vid) ), height, width)

if __name__ == '__main__':
  
  naughty_dict, videos = read_csv_file('../data/label.csv')
  #resize_all_videos(videos, '../data/videos/small/', 200, 150)
  
  # barf out a dir structure 4 gr8 nast
  if not os.path.exists('../data/video_split/'):
    os.mkdir('../data/video_split')
  for key in naughty_dict.keys():
    naughty_path = os.path.join('../data/video_split/',key)
    if not os.path.exists(naughty_path):    
      os.mkdir(naughty_path)

  # main loop, checks for split frames, otherwise uses ffmpeg/avconv to split
  for key in naughty_dict.keys():
    clip_id = 0
    for clip in naughty_dict[key]:
      filename = os.path.basename(clip[0])
      (start, stop) = clip[1:]
      action_out_path = os.path.join('../data/video_split/', key, str(clip_id)+'_'+str(start)+'_'+str(stop)+'.jpg')
      action_vid_path = clip[0]
      clip_id += 1
      print action_out_path, action_vid_path
