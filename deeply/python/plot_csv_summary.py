from process_videos import read_csv_file
import matplotlib.pyplot as plt
import numpy as np

def plot_barz(total_lengths):
  p_row = 4
  p_col = 2
  n = len(total_lengths)
  total_lengths.sort(key=lambda x: x[1], reverse=True)
  val = [num[1] for num in total_lengths] 
  labels = [lab[0].replace('_', ' ') for lab in total_lengths] 
  numplots = p_rows*p_col
  f, axarr = plt.subplots(p_row, p_col)
  f.set_size_inches(15, 30)
  for i in range(p_row):
    for j in range(p_col):
      chunk = n/numplots
      pos = np.arange(chunk) 
      start = j*chunk + i*chunk*p_col
      stop = start + chunk
      if stop > n: 
        stop = n
        pos = np.arange(stop-start)
      rev_vals = val[start:stop]
      rev_labels = labels[start:stop]
      rev_vals.reverse()
      rev_labels.reverse()
      axarr[i,j].barh(pos, rev_vals, align='center')
      axarr[i,j].set_yticks(pos)
      axarr[i,j].set_yticklabels(rev_labels)
  plt.tight_layout()
  f.savefig('../data/category_hist.png', dpi=100)

def sum_of_frames(action_list):
  frames_sum = 0
  for nast_act in action_list:
    frames_sum += nast_act[2] - nast_act[1]
  return frames_sum

if __name__ == '__main__':
  naughty_dict, videos = read_csv_file('../data/label.csv')
  total_lengths = []
  for nasty_key in naughty_dict.keys():
    total_lengths.append((nasty_key,sum_of_frames(naughty_dict[nasty_key])))
  plot_barz(total_lengths)
