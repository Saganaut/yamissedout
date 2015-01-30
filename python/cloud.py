import sys
from optparse import OptionParser
from collections import Counter

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread

def main():
  """main function for standalone usage"""
  usage = "usage: %prog [options] words"
  parser = OptionParser(usage=usage)
  parser.add_option('-d', '--db', default='../db/missed_connections.db',
                    help='DB file [default: %default]')
  parser.add_option('-m', '--mask', default=None, help='Image mask')

  (options, args) = parser.parse_args()

  if len(args) != 1:
      parser.print_help()
      return 2

  with open(args[0]) as f:
      words = [(' '.join(x.split()[:-1]),
                int(x.split()[-1])) for x in f.readlines()]
      if options.mask:
          dickmask = imread(options.mask)
          wordcloud = WordCloud(background_color='white', mask=dickmask)
      else:
          wordcloud = WordCloud()
      wordcloud.fit_words(words)
      wordcloud.to_file('shitdick.png')

if __name__ == '__main__':
    sys.exit(main())
