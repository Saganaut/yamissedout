import sys
from optparse import OptionParser
from collections import Counter

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread

import textstats
import common

#EX: python cloud.py -m ../db/phalice/big_dick.png -c chicago"

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
  parser.add_option('-f', '--font', default='Verdana.ttf', type='string',
                    help='Wordcloud font [default: %default]')
  parser.add_option('-c', '--city', default='atlanta', type='string',
                    help='Wordcloud city [default: %default]')

  (options, args) = parser.parse_args()

  if len(args) != 0 :
    parser.print_help()
    return 2

  if options.city not in common.valid_cities() :
    print "City " + options.city + " is not valid. Choose from:" 
    print '\n'.join(common.valid_cities())
    return 2

  results = textstats.read_from_db(options.db,
                                   num_grams=options.ngram,
                                   maxrecords=options.num_records,
                                   source_city=options.city)
  words = [(' '.join(tokens), count) for (tokens, count) in results]

  if options.mask:
    dickmask = imread(options.mask)
    wordcloud = WordCloud(font_path=options.font, background_color='white', mask=dickmask)
  else:
    wordcloud = WordCloud(font_path=options.font)
  wordcloud.fit_words(words)
  wordcloud.to_file('shitdick.png')

if __name__ == '__main__':
    sys.exit(main())
