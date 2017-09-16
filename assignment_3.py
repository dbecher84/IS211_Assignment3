#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analyze a csv file to find file requests and browser info"""

from __future__ import division
import urllib2
import csv
import re
import datetime
import itertools
import copy
import argparse

PARSER = argparse.ArgumentParser(description='Assignment 3 download file url.')
PARSER.add_argument('--url', action="store", dest="URL")
ARGS = PARSER.parse_args()

#URL = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'

RESPONSE = urllib2.urlopen(ARGS.URL)
RES1, RES2, RES3 = itertools.tee(RESPONSE, 3)

def pic_count(file_info=RES1):
    """Determines how many of the requested files were pictures.
    Args:
        file_info (str): The path to a file to anaylze.
                         default: RES_COUNT

    Returns:
        string: Statement of the percentage of files that were pictures

    Example:
        >>> pic_count(RES1)
        Image requests account for 65.74 percent of all requests.
    """

    file_content_a = csv.reader(file_info)
    files_accessed = []
    tot_files = 0

    pic_pattern = '(jpg|gif|png)$'

    for row in file_content_a:
        tot_files += 1
        pics = re.search(pic_pattern, row[0], re.I)
        if pics:
            files_accessed.append(row[0])

    pic_percent = (int(len(files_accessed))/tot_files)*100
    print 'Image requests account for {0} percent of all requests.'.format(pic_percent)


def pop_browser(file_data=RES2):
    """Finds what drowers was used and calcs the most popular one.
    Args:
        file_data (str): path to the file to be analyzed.
                         default: RES_BROWSER

    Returns:
        string: Statment of the most popular browser

    Example:
        >>> pop_browser(RES2)
        The most popular browser was Chrome.
    """

    file_content_b = csv.reader(file_data)
    chrome = 0
    firefox = 0
    safari = 0
    explorer = 0

    for row in file_content_b:
        w_browser = re.search('MSIE', row[2])
        if w_browser:
            explorer += 1
        f_browser = re.search('Firefox', row[2])
        if f_browser:
            firefox += 1
        c_browser = re.search('Chrome', row[2])
        if c_browser:
            chrome += 1
        s_browser = re.search('Safari', row[2])
        if s_browser:
            if not c_browser:
                safari += 1

    max_test = max(chrome, firefox, explorer, safari)
    winner = 'None'

    if max_test == chrome:
        winner = 'Chrome'
    if max_test == firefox:
        winner = 'Firefox'
    if max_test == explorer:
        winner = 'Internet Explorer'
    if max_test == safari:
        winner = 'Safari'
    print 'The most popular browser was {0}.'.format(winner)


def hourly_hits(enter_url=RES3):
    """Count the number of hits per hour.
    Args:
        URL (str): URL of a csv file to get. default: URL

    Returns:
        string: A statement of the number of hit for each hour of the
                day.
    Example:
        >>> hourly_hits()
        Hour 23 has 0 hits.
        Hour 22 has 0 hits.
        Hour 21 has 0 hits.
        Hour 20 has 0 hits.
        Hour 19 has 0 hits.
        Hour 18 has 0 hits.
        Hour 17 has 0 hits.
        Hour 16 has 0 hits.
        Hour 15 has 0 hits.
        Hour 14 has 0 hits.
        Hour 13 has 0 hits.
        Hour 12 has 0 hits.
        Hour 11 has 0 hits.
        Hour 10 has 0 hits.
        Hour 9 has 0 hits.
        Hour 8 has 0 hits.
        Hour 7 has 0 hits.
        Hour 6 has 0 hits.
        Hour 5 has 994 hits.
        Hour 4 has 1813 hits.
        Hour 3 has 1797 hits.
        Hour 2 has 1795 hits.
        Hour 1 has 1808 hits.
        Hour 0 has 1793 hits.
    """

    hour_of_day = 24
    while hour_of_day:
        res_many = copy.copy(enter_url)
        hour_of_day -= 1
        hour_count = 0
        file_content_h = csv.reader(res_many)
        for row in file_content_h:
            time = datetime.datetime.strptime(row[1],
                                              '%Y-%m-%d %H:%M:%S')
            hour = time.hour
            if hour == hour_of_day:
                hour_count += 1
        print 'Hour {0} has {1} hits.'.format(hour_of_day, hour_count)

if __name__ == "__main__":
    pic_count()
    pop_browser()
    hourly_hits()
