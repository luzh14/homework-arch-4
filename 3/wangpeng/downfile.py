#!/usr/bin/env pyton
#coding=utf-8

import os
import sys
import threading
import urllib2

class ThreadHttp(threading.Thread):
    def __init__(self, url, start_size, end_size, file_name):
        threading.Thread.__init__(self)
        self.url = url
        self.end_size = end_size
        self.start_size = start_size
        self.file_name = file_name
    
    def run(self):
        request = urllib2.Request(self.url)
        savefile = open(self.file_name,'r+')
        request.headers['Range'] = 'bytes=%s-%s' % (self.start_size, self.end_size)
        files = urllib2.urlopen(request).read()
        savefile.seek(self.start_size)
        savefile.write(files)
        savefile.close()

if __name__ == '__main__':
    url = 'http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
    f_name = url.split('/')[-1] 
    if os.path.exists(f_name):
        print 'file exists'
        sys.exit(1)
    os.mknod(f_name)
    size=int(urllib2.urlopen(url).info()['content-length'])
    num = 4
    offset = int( size / num ) + 1
    ranges = []
    for i in xrange(num):
        j = i * offset
        if (j + offset ) > size:
           ranges.append( (j, size))
        else:
            ranges.append( (j, j + offset))
    print ranges
    down_threads = []
    for item_range in ranges:
        start, end = item_range
        th = ThreadHttp(url, start, end, f_name)
        down_threads.append(th)
  
    for t in down_threads:
        t.start()
    for t in down_threads:
        t.join()
