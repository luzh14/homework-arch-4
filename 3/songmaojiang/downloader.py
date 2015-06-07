#!/usr/bin/env python
# coding=utf-8

import sys
import os
import urllib2
import threading


def print_usg():
    print('usage:\n\t' + sys.argv[0] + ' http://URL THREAD_NUM')
    sys.exit(1)

def check_argv():
    if len(sys.argv) != 3:
        print_usg()
    elif not sys.argv[1].startswith('http://'):
        print_usg()
    try:
        num = int(sys.argv[2])
    except:
        print_usg()
    return(sys.argv[1], num)


class downloader(object):
    def __init__(self, p_url, p_num, p_fd):
        self.url, self.num, self.fd = (p_url, p_num, p_fd)

        resp = urllib2.urlopen(self.url).info()
        self.total = int( resp['Content-Length'] )
        self.offset = int( self.total / self.num ) + 1
        if self.offset > 4096:
            self.offset = (self.offset + 4096) / 4096 * 4096
        print('\ninit:\n\tfile size: %d, offset: %d') % (self.total, self.offset)

    def gen_ranges(self):
        '''gen the http header info of range for each threading'''
        ranges = []
        for i in xrange(self.num):
            j = i * self.offset
            if (j + self.offset) > self.total:
                ranges.append( (j, self.total))
            else:
                ranges.append( (j, j + self.offset))
        return(ranges)

    def thread_handler(self, p_start, p_end):
        '''gen a thread to download from p_start to p_end'''
        req = urllib2.Request(self.url)
        req.add_header('Range', 'Bytes=' + str(p_start) + '-' + str(p_end) )
        try:
            resp = urllib2.urlopen(req)
        except:
            print("error when open url: %s", self.url)
            sys.exit(2)

        # write file
        cont = resp.read()
        lock = threading.Lock()
        lock.acquire()
        self.fd.seek(p_start)
        self.fd.write(cont)
        self.fd.flush()
        lock.release()

    def run(self):
        '''main func for this class for running downloader with multi-threading'''
        thread_lists = []
        n = 0
        for item_range in self.gen_ranges():
            start, end = item_range
            print('thread %d - start: %s, end: %s') % (n, start, end)
            thread = threading.Thread(target=self.thread_handler, args=(start, end))
            thread.start()
            thread_lists.append(thread)
            n += 1

        for i in thread_lists:
            i.join()


if __name__ == '__main__':
    url, num = check_argv()
    try:
        same_name = url.split('/')[-1]
    except:
        save_name = './tmp.file'

    with open(same_name, 'w+') as fd:
        down = downloader(url, num, fd)
        down.run()
    print('file: %s download success!' % same_name )

