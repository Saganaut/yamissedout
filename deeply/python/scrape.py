#!/usr/bin/env python
#
# SCRAPE DAT SHIT
#

import sys
from optparse import OptionParser

from pycookiecheat import chrome_cookies
import mechanize
import cookielib
from bs4 import BeautifulSoup
import requests

headers = {'User-agent': 'Mozilla/5.0 (X11; CrOS x86_64 7520.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.110 Safari/537.36'}

def getcookie(cookie_path='~/.config/google-chrome-unstable/Default/Cookies', url='http://ma.brazzers.com'):
    cookie_path = os.path.expanduser(cookie_path)
    return chrome_cookies(url, cookie_file=cookie_path)

def downloadfile(url, cookie):
    outpath = '/tmp/video.mp4'
    r = requests.get(url, stream=True, headers=headers, cookies=cookie)
    with open(outpath, 'wb') as out:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                out.write(chunk)
    return outpath

def dumpvidandlabels(html):
    soup = BeautifulSoup(html, 'html.parser')

    videoname = 'tlib_alessa_savage_ap011416_272p_650_mobile.mp4'

    tag_elements = soup.find_all('li', {'class': 'time-tags-placeholder'})
    for tag_element in tag_elements:
        tag = tag_element.find(class_='timeline-tag-name').text
        for timetag in tag_element.findAll('li', class_='time-tag'):
            start = timetag.attrs['data-start-time']
            end = timetag.attrs['data-end-time']
            print(','.join([videoname, tag, start, end]))

    return soup

def main():
    """main function for standalone usage"""
    usage = "usage: %prog [options] username password"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.print_help()
        return 2

    # do stuff
    pass

#if __name__ == '__main__':
#    sys.exit(main())
