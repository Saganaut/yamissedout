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

def s_to_ffmpeg_ss(seconds):
  m, s = divmod(seconds, 60)
  h, m = divmod(m, 60)
  return str(h)+':'+str(m)+':'+str(s)

def resize_video_strip_sound(filename, output_file, height, width, start, stop):
  command_cut = [ FFMPEG_BIN, 
                '-i',  filename,
                '-ss', s_to_ffmpeg_ss(start),
                '-t', s_to_ffmpeg_ss(stop-start), 
                '-c:v','copy',
                '-an',
                output_file[:-4] + '_temp.mp4']
  sp.call(command_cut)
  command_shrink = [ FFMPEG_BIN,
                    '-i',output_file[:-4] + '_temp.mp4',
                    '-s', '200x150',
                    '-an', 
                    output_file ]
  sp.call(command_shrink)
  os.remove(output_file[:-4] + '_temp.mp4')

def split_clips_resize(naughty_dict, whitelist, height, width):
  if not os.path.exists('../data/video_split/'):
    os.mkdir('../data/video_split')
  # main loop, checks for split frames, otherwise uses ffmpeg/avconv to split
  for key in naughty_dict.keys():
    if not key in whitelist: continue
    clip_id = 0
    for clip in naughty_dict[key]:
      filename = os.path.basename(clip[0])
      (start, stop) = clip[1:]
      action_out_path = os.path.join('../data/video_split/', key+'_'+str(clip_id)+'_'+str(start)+'_'+str(stop)+'.mp4')
      action_vid_path = clip[0]
      clip_id += 1
      print '~~~~Processing: '+ action_vid_path.replace('_', ' ')
      resize_video_strip_sound(action_vid_path, action_out_path, height, width, start, stop);



if __name__ == '__main__':  
  height = 200 
  width = 150
  # Adjust this or read from file to have the classes we want
  whitelist = set(['Test_1', 'Test_2'])
  naughty_dict = read_csv_file('../data/label_fake.csv')
  split_clips_resize(naughty_dict, whitelist, height, width)
  
