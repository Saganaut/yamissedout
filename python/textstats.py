import sys
import os
import sqlite3
import re
import nltk
from nltk.collocations import *

def read_from_db(db_name):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("SELECT body FROM missed_connections")
  num = 0
  line = ""
  regex = re.compile('[^a-zA-Z \']')
  body = cursor.fetchone()
  while body:
    stmt = body[0].strip()
    stmt = stmt.lower()                 #convert all words to lower-case
    stmt = regex.sub(' ', stmt)          #remove symbols
    line += stmt                        #this will crash on a large database but ok for now
    body = cursor.fetchone()

  tokens = line.split()
  bigram_measures = nltk.collocations.BigramAssocMeasures()
  finder = BigramCollocationFinder.from_words(tokens)
  finder.apply_freq_filter(3)
  #print finder.ngram_fd.viewitems()
  #print finder.nbest(bigram_measures.pmi, 100)

  num_grams = 3
  bgs = nltk.ngrams(tokens,num_grams)
  fdist = nltk.FreqDist(bgs)
  for k,v in fdist.most_common(800):
    print ' '.join([str(i) for i in k]), v

  conn.close()



db_path = '../db/missed_connections.db'
if __name__ == '__main__':
  if not os.path.isfile(db_path): 
    print "No missed connections database at " + db_path + "... Run scrape_mc.py first."
    sys.exit()

  read_from_db(db_path)
