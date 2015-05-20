#!/usr/bin/env python
#coding=utf-8

import os
import sys
import time
import threading
import urllib2

class ThreadHttp(threading.Thread):
    '''使用线程下载http
    '''
    def __init__(self, url, start_size, end_size, file_name):
        threading.Thread.__init__(self)
        self.url = url
        self.start_size = start_size
        self.end_size = end_size
        self.file_name =  file_name
    
    def run(self):
        request = urllib2.Request(self.url)
        savefile =  open(self.file_name, 'r+')
        # 使用HTTP Range进行下载分片
        request.headers['Range'] = 'bytes=%s-%s' % (self.start_size, self.end_size)
        files = urllib2.urlopen(request).read()
        savefile.seek(self.start_size)
        savefile.write(files)
        savefile.close()

class DownRate(threading.Thread):
    '''显示下载进度
    '''
    def __init__(self, size, file_name):
        threading.Thread.__init__(self)
        self.size = size
        self.file_name = file_name
    
    def run(self):
        while True:
            real_size = os.path.getsize(self.file_name)
            percent = float(real_size)/float(self.size)*100
            m_size = str(real_size/1048576)
            print '\r'+ "download " + self.file_name +' '+ m_size +'M', "%.2f%%" % (percent),
            sys.stdout.flush()
            time.sleep(0.1)
            if self.size <= real_size:
                break

def downlaod(url, thread):
    # 获取文件大小，并简单判断是不是一个正确的URL
    try:
        response = urllib2.urlopen(url)
        response.close()
        size = int(response.info()['content-length'])
    except Exception,e:
        print 'Please enter a http url or http url timeout'
        sys.exit()
    
    # 根据进程数分片
    quotient, remainder = divmod(int(size), thread)
    size = size - remainder 
    size_list = [(n+1, n+quotient) for n in xrange(0, size, quotient)]
    size_list[0] = (0,size_list[0][1])
    if remainder != 0:
        size_list[-1] = (size_list[-1][0], size_list[-1][1]+remainder)    
   
    # 创建文件 检查文件是否存在
    file_name = url.split('/')[-1]
    if os.path.exists(file_name):
        print  file_name + 'file exists'
        sys.exit(1)
    os.mknod(file_name)

    # 添加线程
    down_list = []
    down_list.append(DownRate(size, file_name))
    for h_range in size_list:
        t = ThreadHttp(url, h_range[0], h_range[1], file_name)
        down_list.append(t)
    
    # 运行线程
    for h in down_list:
        h.start()
    for h in down_list:
        h.join()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser("HTTP download")
    parser.add_argument(
            '-u', action='store', 
            dest='url', help='http url address'
    )   
    parser.add_argument(
            '-t', action='store', dest='thread', 
            type=int,default=5, help='thread count default is 5'
    )
    results = parser.parse_args()
    
    if not results.url:
        print '***url can not be empty***'
        parser.print_help()
        sys.exit()
    url = results.url
    thread = results.thread

    downlaod(url, thread)
