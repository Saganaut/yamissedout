import sqlite3
import os.path
import sys

import requests

from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin

# The base url for craigslist in New York
BASE_URL = 'http://atlanta.craigslist.org/search/mis'
num_pages = 1

#viable classes 
mc_classes = set(['w4m', 'm4m', 'm4w', 'w4w', 't4m', 'm4t', 't4w', 'w4t', 't4t', 'mw4mw', 'mw4w', 'mw4m', 'w4mw', 'm4mw', 'w4ww', 'm4mm', 'mm4m', 'ww4w', 'ww4m', 'mm4w', 'm4ww', 'w4mm', 't4mw', 'mw4t'])

def scrape_mc():
  
  for i in range(num_pages):
    mc_data = []
    print "---Processing Page " + str(i)
    offset = ("?s=" + str(i*100)) if i > 0 else ""
    response = requests.get(BASE_URL + offset)
    soup = BeautifulSoup(response.content)
    missed_connections = soup.find_all('span', {'class':'pl'})
    c = 0
    for missed_connection in missed_connections:
      sys.stdout.write("--Progress: %d%%   \r" % (c) )
      sys.stdout.flush()
      c+=1
      link = missed_connection.find('a').attrs['href']
      url = urljoin(BASE_URL, link)
      mc_data.append(extract_mc_features(url))
      # break
    print "---Writing Page " + str(i) + " to Db"
    write_chunk_to_db(mc_data)
    

def extract_mc_features(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content)
  mc_data = extract_subject_features(soup.find('h2', {'class':'postingtitle'}).text.strip())
  mc_data['datetime'] = soup.find('time').attrs['datetime']
  mc_data['raw_subject'] = soup.find('h2', {'class':'postingtitle'}).text.strip().replace("\"", "\'")
  mc_data['body'] = soup.find('section', {'id':'postingbody'}).text.strip().replace("\"", "\'")
  mc_data['url'] = url
  return mc_data

def extract_subject_features(subject):
  mc_data = {}
  location, new_subject  = get_location(subject)
  mc_data['location'] = location
  split_subject = new_subject.split(' - ')

  mc_data['age'], split_subject = get_age(split_subject)
  mc_data['mc_class'], split_subject = get_class(split_subject)
  mc_data['subject'] = ', '.join(split_subject[:])
  print str(mc_data['subject'])
  
  mc_data['gender'] = mc_data['mc_class'][0] if mc_data['mc_class'] != 'unknown' else 'unknown'
  print mc_data
  return mc_data

def get_location(subj):
  """ Extract the location from the subject line. May do more sophisticated guessing later. """
  if '(' in subj:
    location = subj[subj.find("(")+1:subj.find(")")]
    subj = subj[:subj.find("(")] +  subj[subj.find(")")+1:]
    return location.replace("\"", "\'"), subj
  else:
    return 'unknown', subj

def get_age(subj):
  str_len = len(subj)
  if subj[str_len - 1].isdigit():
    return int(subj[str_len - 1]), subj[0:str_len-2]
  else:
    return -1, subj

def get_class(subj):
  str_len = len(subj)
  if subj[str_len - 1].strip() in mc_classes:
    return subj[str_len - 1].strip(), subj[0:str_len-2]
  else:
    return 'unknown', subj

def write_database(db_name):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("""CREATE TABLE missed_connections (datetime text, raw_subject text, subject text, body text, url text, mc_class text, location text, age real, gender text)""")
  conn.commit()
  conn.close()

  
def write_chunk_to_db(data, db_name='../db/missed_connections.db'):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  for row in data:
    # c.execute("INSERT INTO missed_connections VALUES ('2006-01-05','BUY','RHAT',100,35.14)")   
    print("INSERT INTO missed_connections  VALUES (\""+row["datetime"]+"\",\""+row["raw_subject"]+"\",\""+row["subject"]+"\",\""+row["body"]+"\",\""+row["url"]+"\",\""+row["mc_class"]+"\",\""+row["location"]+"\","+str(row["age"])+",\""+row["gender"]+"\")")
    cursor.execute("INSERT INTO missed_connections VALUES (\""+row["datetime"]+"\",\""+row["raw_subject"]+"\",\""+row["subject"]+"\",\""+row["body"]+"\",\""+row["url"]+"\",\""+row["mc_class"]+"\",\""+row["location"]+"\","+str(row["age"])+",\""+row["gender"]+"\")")
    conn.commit()
  conn.close()

if __name__ == '__main__':
  if not os.path.isfile('../db/missed_connections.db'): 
    write_database('../db/missed_connections.db')
  scrape_mc()













