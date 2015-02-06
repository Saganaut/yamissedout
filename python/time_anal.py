from collections import defaultdict
import sys
import os
import sqlite3
import time
import datetime
import csv

db_path = '../db/missed_connections.db'


def time_analysis(db_name, gender='m'):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("SELECT datetime FROM missed_connections WHERE gender = \'"+gender+"\'")  
  rows = cursor.fetchall()
  dates = []
  time_appearances = defaultdict(int)
  date_appearances = defaultdict(int)
  for i in range(24):
    time_appearances[str(i).zfill(2)]
    date_appearances[str(i).zfill(2)]
  for row in rows:
    date = time.strftime("%a", time.strptime(row[0][0:-14], "%Y-%m-%d"))
    just_time = time.strftime("%H", time.strptime(row[0][11:-5], "%H:%M:%S"))
    time_appearances[just_time]+=1
    date_appearances[date]+=1


  with open('../web/web_data/male_time.tsv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\t',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["time","frequency"])
    sorted_keys = sorted(time_appearances.keys())
    for k in sorted_keys:
      spamwriter.writerow([k, time_appearances[k]])


if __name__ == '__main__':
  if not os.path.isfile(db_path): 
    print "No missed connections database at " + db_path + "... Run scrape_mc.py first."
  time_analysis(db_path)
