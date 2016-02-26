#!/usr/bin/env python
#
# SCRAPE DAT SHIT
#

import sys
from optparse import OptionParser
import time
import os

from pycookiecheat import chrome_cookies
from bs4 import BeautifulSoup
import requests

headers = {'User-agent': 'Mozilla/5.0 (X11; CrOS x86_64 7520.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.110 Safari/537.36'}

def getcookie(cookie_path='~/.config/google-chrome-unstable/Default/Cookies', url='http://ma.brazzers.com'):
    cookie_path = os.path.expanduser(cookie_path)
    return chrome_cookies(url, cookie_file=cookie_path)

def downloadfile(url, outpath, cookie):
    r = requests.get(url, stream=True, headers=headers, cookies=cookie)
    with open(outpath, 'wb') as out:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                out.write(chunk)
    return outpath

def _videoname(url):
    if url.endswith('/'):
        url = url[:-1]
    scenetitle = os.path.basename(url)
    return '%s.mp4' % scenetitle

def dumpvidandlabels(url, cookie, videodir='videos'):
    r = requests.get(url, headers=headers, cookies=cookie)

    sys.stderr.write('Status code: %d\n' % r.status_code)
    if r.status_code == 404:
        sys.stderr.write(r.text)
        return

    soup = BeautifulSoup(r.text, 'html.parser')

    try:
        if soup.title.text == 'Brazzers Members Area  Worlds Best HD Pornsite':
            sys.stderr.write('Cookie has expired! Relogin on Chrome\n')
            sys.exit(1)
    except AttributeError:
        sys.stderr.write('Error loading page!\n')
        sys.stderr.write(r.text)
        sys.exit(1)

    videourl = 'http://ma.brazzers.com' + soup.findAll('a', target='_blank', class_='clearfix download-full')[-1].attrs['href']
    videopath = os.path.join(videodir, _videoname(url))

    tag_elements = soup.find_all('li', {'class': 'time-tags-placeholder'})
    for tag_element in tag_elements:
        tag = tag_element.find(class_='timeline-tag-name').text
        for timetag in tag_element.findAll('li', class_='time-tag'):
            start = timetag.attrs['data-start-time']
            end = timetag.attrs['data-end-time']
            print(','.join([videopath, url, tag, start, end]))

    sys.stderr.write('Downloading %s to %s...\n' % (videourl, videopath))
    downloadfile(videourl, videopath, cookie)
    sys.stderr.write('Downloading complete!\n')

def main():
    """main function for standalone usage"""
    usage = "usage: %prog [options] urlfile > label.csv 2> log"
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--cookie-path', default='~/.config/google-chrome-unstable/Default/Cookies',
                      help='Path to Chrome cookies sqlite DB [default: %default]')
    parser.add_option('-v', '--video-dir', default='videos',
                      help='Path to video directory [default: %default]')

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return 2

    try:
        os.mkdir(options.video_dir)
    except OSError:
        pass

    # do stuff
    cookie = getcookie(cookie_path=options.cookie_path)
    sys.stderr.write('Using cookie: %s\n' % str(cookie))
    with open(args[0]) as f:
        for url in f:
            url = url.strip()
            sys.stderr.write('Extracting video and features for %s...\n' % url)
            dumpvidandlabels(url, cookie, videodir=options.video_dir)
            time.sleep(10)

if __name__ == '__main__':
    sys.exit(main())
