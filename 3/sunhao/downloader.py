#!/usr/bin/env python
# coding=utf-8
import urllib2
import os
from threading import Thread
import shutil 
import sys
import time
import requests

def get_terminal_size(fd=1):
    """
    Returns height and width of current terminal. First tries to get
    size via termios.TIOCGWINSZ, then from environment.
    Arguments:
    - `fd`: file descriptor (default: 1=stdout)
    """
    hw = (0, 0)
    if os.isatty(fd):
        try:
            import fcntl
            import termios
            import struct
            hw = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            try:
                hw = (os.environ['LINES'], os.environ['COLUMNS'])
            except:
                pass
    return hw

def progressbar(total_volume, completed_volume, progress=0):
    """A simple progressbar.
    Arguments:
    - `total_volume`: int, total volume size.
    - `completed_volume`: int, completed volume size.
    - `progress`: int, completed percent.
    """
    progress = completed_volume / float(total_volume) * 100
    base = get_terminal_size()[1] / 2
    current = int(progress / 100 * base)
    info = u'\r[ %s%s Total: %-8d Completed: %.2f%% ]' % (
        current * '#',
        (base - current) * ' ',
        total_volume,
        progress)
    sys.stdout.write(info)
    sys.stdout.flush()
    time.sleep(0.3)

class FlitRequest(object):
    def __init__(self,opener):
        self._opener = opener
    def get_url_response(self,url_req):
        is_error = False
        if not url_req:
            raise requests.URLRequired
        try:
            #resp = self._opener.open(url_req,timeout=10)
            resp = self._opener.open(url_req)
        except (urllib2.HTTPError,urllib2.URLError),why:
            print why
            is_error = True
            return (why,is_error)
        else:
            return (resp,is_error)
    def get_url_chunk(self,url_req):
        resp,is_error = self.get_url_response(url_req)
        response = dict()
        response['url'] = resp.geturl()
        response['status_code'] = 1 and resp.getcode() or None
        response['headers'] = resp.info()
        response['charset'] = response['headers'].getparam('charset')
        if is_error:
            response['error'] = resp
        #print response
        return response 
    def get_url_headers(self,url_req):
        chunk = self.get_url_chunk(url_req)
        if chunk.get('error',''):
            return None
        return chunk['headers']        
    def get_url_size(self,url_req):
        headers = self.get_url_headers(url_req)
        if not headers:
            return 0
        content_length = headers.getheaders('Content-Length')
        length = int(content_length[0]) or 0
        return length
    def get_file_name(self,url_req):
        filename = url_req.split('/')[-1]
        return filename
class SegmentsThread(Thread):
    def __init__(self,opener,url_req,filename,ranges=0):
        Thread.__init__(self)
        self.daemon = True
        self._opener = opener
        self._url_req = url_req
        self._filename = filename
        self._ranges = ranges
        self.fetched = 0 
    def run(self):
        try:
            self.fetched = os.path.getsize(self._filename)
        except OSError:
            self.fetched = 0
        self.startmark = self._ranges[0] + self.fetched
        if self.startmark >= self._ranges[1]:
            return
        self.size_per_time = 16384
        req = urllib2.Request(self._url_req)
        req.add_header("Range","bytes=%d-%d" %(self.startmark,self._ranges[1]))
        self.chunkhandle = self._opener.open(req)
        chunk = self.chunkhandle.read(self.size_per_time)
        while chunk:
            file = open(self._filename,'ab+')
            try:
                file.write(chunk)
            except Exception,err:
                print "can't write %s:" %self.filename,err
            finally:
                file.close()
            self.fetched += len(chunk)
            chunk = self.chunkhandle.read(self.size_per_time)
class MultiSegment(object):
    def __init__(self,opener):
        self._opener = opener
        self.filter = FlitRequest(self._opener)
    def split_segment(self,url_size,segment_number):
        segment_size = url_size/segment_number
        ranges = [ (i*segment_size,(i+1)*segment_size-1)for i in xrange(segment_number-1) ]
        ranges.append((segment_size*(segment_number-1),url_size-1)) 
        return ranges
    def _isalive(self,tasks):
        for task in tasks:
            if task.isAlive():
                return True
        return False
    def __call__(self,url_req,segments = 2):
        url_size = self.filter.get_url_size(url_req)
        if not url_size:
            raise requests.RequestException("Couldn't get file size from url\n[URL]: %s" % url_req)
        ranges = self.split_segment(url_size,segments) 
        output = self.filter.get_file_name(url_req)
        filename = [ "%s_tmp_%d.pfd" %(output,i) for i in xrange(segments)]
        tasks = []
        for i in xrange(segments):
            task = SegmentsThread(self._opener,url_req,filename[i],ranges[i])
            task.start()
            tasks.append(task)
        time.sleep(0.5)
        while self._isalive(tasks):
            fetched = sum([t.fetched for t in tasks]) 
            progressbar(url_size, fetched)
        fileobj = open(output,'wb+')
        try:
            for i in filename:
                with open(i,'rb') as f:
                    shutil.copyfileobj(f,fileobj)
                    os.remove(i)
        finally:
            fileobj.close()
        finished_size = os.path.getsize(output)
        if abs(url_size - finished_size) <= 10:
            progressbar(url_size,finished_size,100) 
                      
if __name__ == '__main__':
    url_req = 'http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe' 
    segment_number = 3
    opener = urllib2.build_opener()
    first = MultiSegment(opener)
    first(url_req,segment_number)
