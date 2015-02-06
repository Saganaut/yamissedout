import sys
import os
import sqlite3
import re
import nltk
from optparse import OptionParser
from nltk.collocations import *

def read_from_db(db_name, num_grams=3, maxrecords=40):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("SELECT body FROM missed_connections")
  num = 0
  lines = []
  regex = re.compile('[^a-zA-Z \']')
  body = cursor.fetchone()
  while body:
    stmt = body[0].strip()
    stmt = stmt.lower()                 #convert all words to lower-case
    stmt = regex.sub(' ', stmt)          #remove symbols
    lines.append(stmt)             
    body = cursor.fetchone()

  conn.close()
  
  line = ''.join(lines)
  #entity_extraction(line)
  tokens = line.split()
  bigram_measures = nltk.collocations.BigramAssocMeasures()
  finder = BigramCollocationFinder.from_words(tokens)
  finder.apply_freq_filter(3)

  bgs = nltk.ngrams(tokens,num_grams)
  fdist = nltk.FreqDist(bgs)
  return fdist.most_common(maxrecords)

def entity_extraction(document):
  #if this crashes run 'python -m nltk.downloader all'
  sentences = nltk.sent_tokenize(document)
  sentences = [nltk.word_tokenize(sent) for sent in sentences]
  sentences = [nltk.pos_tag(sent) for sent in sentences]
  grammar = "NP: {<DT>?<JJ>*<NN>}"
  cp = nltk.RegexpParser(grammar)
  result = cp.parse(sentences[0])
  print(result)
  exit()

def main():
  """main function for standalone usage"""
  usage = "usage: %prog [options] input"
  parser = OptionParser(usage=usage)
  parser.add_option('-d', '--db-name', default='../db/missed_connections.db', type='string',
                    help='Database name BITCH [default: %default]')
  parser.add_option('-n', '--num-grams', default=3, type='int',
                    help='Number of grams for the n-gram BITCH [default: %default]')
  parser.add_option('-m', '--max-records', default=40, type='int',
                    help='Max number of records to parse from the db BITCH [default: %default]')

  (options, args) = parser.parse_args()

  if (len(args) != 0) :#or (options.num_pages <= 0) or (options.extract_pics not in (0,1)) :
    parser.print_help()
    return 2

  db_path = options.db_name
  if not os.path.isfile(db_path): 
    print "No missed connections database at " + db_path + "... Run scrape_mc.py first."

  for k,v in read_from_db(db_name=options.db_name, num_grams=options.num_grams, maxrecords=options.max_records):
    print ' '.join([str(i) for i in k]), v


if __name__ == '__main__':
    sys.exit(main())
