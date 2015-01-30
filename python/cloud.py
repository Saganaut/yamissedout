import sys
from optparse import OptionParser
from collections import Counter

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread

import textstats

def main():
  """main function for standalone usage"""
  usage = "usage: %prog [options]"
  parser = OptionParser(usage=usage)
  parser.add_option('-d', '--db', default='../db/missed_connections.db',
                    help='DB file [default: %default]')
  parser.add_option('-m', '--mask', default=None, help='Image mask')
  parser.add_option('-n', '--ngram', default=3, type='int',
                    help='n for n-grams [default: %default]')
  parser.add_option('-r', '--num-records', default=800, type='int',
                    help='Max number of records [default: %default]')

  (options, args) = parser.parse_args()

  if len(args) != 0:
      parser.print_help()
      return 2

  results = textstats.read_from_db(options.db,
                                   num_grams=options.ngram,
                                   maxrecords=options.num_records)
  words = [(' '.join(tokens), count) for (tokens, count) in results]
  
  if options.mask:
    dickmask = imread(options.mask)
    wordcloud = WordCloud(background_color='white', mask=dickmask)
  else:
    wordcloud = WordCloud()
  wordcloud.fit_words(words)
  wordcloud.to_file('shitdick.png')

if __name__ == '__main__':
    sys.exit(main())
