import sys
import os
import sqlite3
import re
import nltk
from nltk.collocations import *

def read_from_db(db_name, num_grams=3, maxrecords=800):
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

  conn.close()

  tokens = line.split()
  bigram_measures = nltk.collocations.BigramAssocMeasures()
  finder = BigramCollocationFinder.from_words(tokens)
  finder.apply_freq_filter(3)

  bgs = nltk.ngrams(tokens,num_grams)
  fdist = nltk.FreqDist(bgs)
  return fdist.most_common(maxrecords)

db_path = '../db/missed_connections.db'
if __name__ == '__main__':
  if not os.path.isfile(db_path): 
    print "No missed connections database at " + db_path + "... Run scrape_mc.py first."

  for k,v in read_from_db(db_path):
    print ' '.join([str(i) for i in k]), v
