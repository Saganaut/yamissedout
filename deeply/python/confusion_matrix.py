import numpy as np
import matplotlib.pyplot as plt
import csv

def draw_colormap(conf_arr,labels, show_percent=False):
  norm_conf = []
  row_sums = np.sum(conf_arr, axis=1)
  for i in conf_arr:
    a = 0
    tmp_arr = []
    a = sum(i, 0)
    for j in i:
      tmp_arr.append(float(j)/float(a))
    norm_conf.append(tmp_arr)
  fig = plt.figure()
  plt.clf()
  ax = fig.add_subplot(111)
  ax.set_aspect(1)
  res = ax.imshow(np.array(norm_conf), cmap='viridis', 
                  interpolation='nearest')
  width, height = conf_arr.shape
  for x in xrange(width):
    for y in xrange(height):
      if show_percent:
       ax.annotate("{0:.2f}".format(conf_arr[x][y]/float(row_sums[x])*100), xy=(y, x), 
                    horizontalalignment='center',
                    verticalalignment='center')
      else:
        ax.annotate(str(conf_arr[x][y]), xy=(y, x), 
                    horizontalalignment='center',
                    verticalalignment='center')

  cb = fig.colorbar(res)
  plt.xticks(range(width), labels[:width])
  plt.yticks(range(height), labels[:height])
  plt.show()
#plt.savefig('../data/confusion_matrix.png', format='png')


if __name__ == '__main__':
  with open('../data/active_classes.csv', 'rb') as f:
    label_reader = csv.reader(f, delimiter=',')
    labels = label_reader.next()
    conf_arr = np.array([[33,112,0,0,0,0,0,0,0,1,3], 
              [3,31,0,0,0,0,0,0,0,0,0], 
              [0,4,41,0,0,0,0,0,0,0,1], 
              [0,1,0,30,0,6,0,0,0,0,1], 
              [0,0,0,0,38,10,0,0,0,0,0], 
              [0,0,0,3,1,39,0,0,0,0,4], 
              [0,2,2,0,4,1,31,0,0,0,2],
              [0,1,0,0,0,0,0,36,0,2,0], 
              [0,0,0,0,0,0,1,5,37,5,1], 
              [3,0,0,0,0,0,0,0,0,39,0], 
              [0,0,0,0,0,0,0,0,0,0,38]])
    draw_colormap(conf_arr,labels, show_percent=True)
