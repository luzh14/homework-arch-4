#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'luke'


import urllib,urllib2
import os
from threading import Thread

def GetFileSize(url):

    try:
        request = urllib2.urlopen(url)
        request._method = 'HEAD'
        meta=request.info()

    except Exception as e:
        print ('%s %s' % (url,e ))
    else:
        return meta.get_headers('Content-Length')[0]

def SpliteBlocks(totalsize, blocknumber):
    totalsize=int(totalsize)
    blocksize = int(totalsize / blocknumber)
    ranges = []
    for i in range(0, blocknumber - 1):
        ranges.append((i * blocksize, i * blocksize + blocksize - 1))
    ranges.append((blocksize * (blocknumber - 1), totalsize - 1))

    return ranges

def CombineFile(downloadFile,tmpFileList):
    filehandle = open(downloadFile, 'wb+')
    for i in tmpFileList:
        f = open(i, 'rb')
        filehandle.write(f.read())
        f.close()
        try:
            os.remove(i)
            pass
        except:
            pass

    filehandle.close()

class DownLoader(Thread):
    def __init__(self,threadname, url, filename, range):
        Thread.__init__(self)
        self.name = threadname
        self.url = url
        self.filename = filename
        self.range = range

    def run(self):
        req=urllib2.urlopen(self.url)
        start_sign=int(self.range[0])
        end_sign=int(self.range[1])
        req.headers['Range'] = 'bytes=%d-%d' % (start_sign, end_sign)
        fobj=open(self.filename,'wb+')
        block_size=end_sign-start_sign+1
        fobj.seek(start_sign)
        fobj.write(req.read(block_size))
        fobj.close()


if __name__ == '__main__':
    url='http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
    downloadFile='download.file'
    blocks=7
    size = GetFileSize(url)
    ranges = SpliteBlocks(size, blocks)
    threadname = ["thread_%d" % i for i in range(0, blocks)]
    tmpFileList = ["tmpfile_%d" % i for i in range(0, blocks)]
    taskList=[]
    for i in range(blocks):
        task=DownLoader(threadname[i],url,downloadFile,ranges[i])
        taskList.append(task)
    for t in taskList:
        t.start()
    for t in taskList:
        t.join()

    #CombineFile(downloadFile,tmpFileList)