#!/bin/python
#encoding=utf-8

import sys
import os
import time
import urllib
from threading import Thread,Lock
import shutil
from contextlib import closing
from __builtin__ import True

printLocker = Lock()

class AxelPython(Thread,urllib.FancyURLopener):
    
    def __init__(self,threadname,url,filename,ranges):
        Thread.__init__(self,name=threadname)
        urllib.FancyURLopener.__init__(self)
        self.name = threadname
        self.url = url
        self.filename = filename
        self.ranges = ranges
        self.downloaded = 0 
    
    
    def run(self):
        try:
            self.downloaded = os.path.getsize(self.filename)
        except OSError:
            self.downloaded = 0
        
        self.startpoint = self.ranges[0] + self.downloaded
        
        if self.startpoint >= self.ranges[1]:
            print 'Part %s has been downloaded over.' %self.filename
            
            return 
        self.oneTimeSize = 16384
        printLocker.acquire()
        print 'task %s will download from %d to %d' %(self.name,self.startpoint,self.ranges[1])
        
        printLocker.release()
        self.addheader("Range","bytes=%d-%d" %(self.startpoint,self.ranges[1]))
        
        self.urlhandle = self.open(self.url)
        
        data = self.urlhandle.read(self.oneTimeSize)
        
        while data:
            
            filehandle = open(self.filename,'ab+')
            filehandle.write(data)
            filehandle.close()
            
            self.downloaded += len(data)
            
            data = self.urlhandle.read(self.oneTimeSize)
            
def GetUrlFileSize(url):
    with closing(urllib.urlopen(url)) as urlHandler:
        length = urlHandler.headers.getheader('Content-Length')
        if length is None:
            return 0
        else:
            return int(length)
         
def SpliteBlocks(totalsize, blocknumber):
    blocksize = totalsize / blocknumber
    ranges = []
    for i in range(0, blocknumber - 1):
        ranges.append((i * blocksize, i * blocksize + blocksize - 1))
    ranges.append((blocksize * (blocknumber - 1), totalsize - 1))
        
    return ranges

def islive(tasks):
    for task in tasks:
        if task.isAlive():
            return True
    return False

def paxel(url,output,blocks=6):
    size = GetUrlFileSize(url)
    ranges = SpliteBlocks(size, blocks)
    
    threadname = ["thread_%d" %i for i in range(0,blocks)]
    filename = ["tmpfile_%d" %i for i in range(0,blocks)]
    
    tasks = []
    
    for i in range(0,blocks):
        task = AxelPython(threadname[i],url,filename[i],ranges[i])
        
        task.setDaemon(True)
        task.start()
        tasks.append(task)
    time.sleep(2)
    while islive(tasks):
        downloaded = sum([task.downloaded for task in tasks])
        process  = downloaded / float(size) * 100
        show = u'\r Filesize:%d Downloaded:%d Completed:%.2f%%' %(size,downloaded,process)
        sys.stdout.write(show)
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write(u'\rFilesize:{0}  Download:{0} Completed:100% \n'.format(size))
    sys.stdout.flush()
    
    with open(output,'wb+') as filehandle:
        for i in filename:
            with open(i,'rb') as f:
                shutil.copyfileobj(f,filehandle,102400)
            try:
                os.remove(i)
            except OSError:
                pass
if __name__ == '__main__':
    url = 'http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
    output = 'download.file'
    paxel(url,output,blocks=4)       
