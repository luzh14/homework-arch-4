#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'luke'


import urllib2
import os
from threading import Thread

def GetFileSize(url, proxy=None):
    """通过content-length头获取文件大小
    url - 目标文件URL
    proxy - 代理
    """
    opener = urllib2.build_opener()
    if proxy:
        if url.lower().startswith('https://'):
            opener.add_handler(urllib2.ProxyHandler({'https' : proxy}))
        else:
            opener.add_handler(urllib2.ProxyHandler({'http' : proxy}))
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        response = opener.open(request)
        response.read()
    except Exception, e:
        print '%s %s' % (url, e)
    else:
        return dict(response.headers).get('content-length', 0)

def SpliteBlocks(totalsize, blocknumber):
    totalsize=int(totalsize)
    blocksize = totalsize / blocknumber
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
        req=urllib2.Request(self.url)
        start_size=self.range[0]
        end_size=self.range[1]
        req.headers['Range'] = 'bytes=%d-%d' % (start_size, end_size)
        f = urllib2.urlopen(req)
        block=f.read(self)
        fobj=open(self.filename,'wb')
        fobj.write(block)
        fobj.close()


if __name__ == '__main__':
    url='http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
    downloadFile='download.file'
    blocks=5
    size = GetFileSize(url)
    ranges = SpliteBlocks(size, blocks)
    threadname = ["thread_%d" % i for i in range(0, blocks)]
    tmpFileList = ["tmpfile_%d" % i for i in range(0, blocks)]
    taskList=[]
    for i in range(blocks):
        taskList.append(DownLoader(threadname[i],url,tmpFileList[i]),ranges[i])
    for t in taskList:
        t.start()
    for t in taskList:
        t.join()
    CombineFile(downloadFile,tmpFileList)