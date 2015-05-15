#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
author: kakaxi
version: 0.1
create_time: 2015/05/13
"""

import requests
import threading

url="http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe"
n = 8
filename="QQ7.exe"
fd = file(filename, "wb+")
def getLength(url):
    head = requests.head(url)
    return head.headers.get("content-length", 0)

def splitLength(filesize, n):
    step = int(filesize) / n
    lastbytes = int(filesize) % n
    ranges = [[i, i+step-1] for i in range(0, int(filesize), step)]
    if lastbytes != 0:
        ranges[-1][-1] = ranges[-1][0]+lastbytes-1
    print ranges
    return ranges

def getSplitFile(*Range):
    Range_str = "bytes=%s-%s" % Range
    global url
    header = {'Range':Range_str}
    req = requests.get(url, headers=header)
    
    saveSplitToFile(req.content, Range)


def saveSplitToFile(*splitinfo):
    (content, Range) = splitinfo
    global filename
    global fd
    fd.seek(Range[0])
    print fd.tell()
    fd.write(content)
    fd.flush()

def main():
    global url
    filesize = getLength(url)
    ranges =  splitLength(filesize, 8)

    for i in range(0, 8):
        t = threading.Thread(target=getSplitFile, args=(ranges[i]))
        t.start()
main()


