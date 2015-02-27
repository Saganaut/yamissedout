from collections import defaultdict
import sys
import os
import sqlite3
import time
import datetime
import csv

import common

db_path = '../db/missed_connections.db'


def time_analysis(db_name, gender='m', city=None):
  gender_str = {'m':'male', 'w':'female', 't':'trans'}
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  if city == None or city == 'all':
    cursor.execute("SELECT datetime FROM missed_connections WHERE gender = \'"+gender+"\'")  
  else:
    cursor.execute("SELECT datetime FROM missed_connections WHERE gender = \'"+gender+"\' AND city = \'"+city+"\' ")  
  rows = cursor.fetchall()
  n_peepz = len(rows)
  dates = []
  time_appearances = defaultdict(int)
  date_appearances = defaultdict(int)
  for i in range(24):
    time_appearances[str(i).zfill(2)]
    
  for row in rows:
    date = time.strftime("%a", time.strptime(row[0][0:-14], "%Y-%m-%d"))
    just_time = time.strftime("%H", time.strptime(row[0][11:-5], "%H:%M:%S"))
    time_appearances[just_time]+=1
    date_appearances[date]+=1

  if city == None:
    city = ""
  else:
    city+="_"
  with open('../web/web_data/'+city+gender_str[gender]+'_time.tsv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\t',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if n_peepz == 0:
      spamwriter.writerow(["[]"])
    else:
      spamwriter.writerow(["time","frequency","count"])
      sorted_keys = sorted(time_appearances.keys())
      for k in sorted_keys:
        spamwriter.writerow([k, time_appearances[k]/float(n_peepz), time_appearances[k]])

  with open('../web/web_data/'+city+gender_str[gender]+'_days.tsv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\t',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if n_peepz == 0:
      spamwriter.writerow(["[]"])
    else:
      spamwriter.writerow(["time","frequency","count"])
      sorted_keys = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
      for k in sorted_keys:
        spamwriter.writerow([k, date_appearances[k]/float(n_peepz), date_appearances[k]])

def process_cities():
  for city in common.valid_cities():
    print city
    time_analysis(db_path, 'm', city)
    time_analysis(db_path, 'w', city)
    time_analysis(db_path, 't', city)
  time_analysis(db_path, 'm')
  time_analysis(db_path, 'w')
  time_analysis(db_path, 't')

if __name__ == '__main__':
  if not os.path.isfile(db_path): 
    print "No missed connections database at " + db_path + "... Run scrape_mc.py first."
  else:
    process_cities()
    time
  

