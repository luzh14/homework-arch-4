#!/usr/bin/env python
#coding = utf-8
#author = julong
import urllib,urllib2,re
from threading import Thread,Lock
from  multiprocessing.dummy import Pool as ThreadPool
import os,sys,time
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer

lock = Lock()
updatesize=0
class downFileMul(Thread):
    def __init__(self,url,User_agent,run_bar,start,finish,fb):
        self.url = url
        self.User_agent = User_agent
        self.run_bar = run_bar
        self.start_seek = start
        self.end_seek = finish
        self.fb = fb
        Thread.__init__(self)
    def run(self):
        global updatesize
        req = urllib2.Request(self.url)
        req.headers['User-Agent'] =self.User_agent
        req.headers['Range'] = 'bytes=%s-%s'%(self.start_seek,self.end_seek)
        f = urllib2.urlopen(req)
        while 1:
            date = f.read()
            if not date:
                break
            with lock:
                self.fb.seek(self.start_seek)
                self.fb.write(date)
                updatesize += len(date)
                self.run_bar.update(updatesize)
def main(url,User_agent,thread = 5):
    regex = re.compile(r'^(?:http|ftp)s?://'r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'r'localhost|'r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'r'(?::\d+)?'r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not regex.match(url):
        print "%s is not a effective url"%url
        return
    filename = urllib2.unquote(url).decode('utf8').split('/')[-1]
    req = urllib2.Request(url)
    req.headers['User-Agent'] =User_agent
    f=urllib2.urlopen(req)
    size = int(f.info().getheaders('Content-Length')[0])
    widgets = ['Test: ', Percentage(), ' ',Bar(marker='>',left='[',right=']'), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=size)
    fb = open(filename,"wb+")
    block_size = size % thread + 1
    thread_list = []
    for i in range(thread):
        start_file_seek = i*block_size
        end_file_seek = start_file_seek + block_size
        if i == thread - 1:
            end_file_seek = ''
        t = downFileMul(url,User_agent,pbar,start_file_seek,end_file_seek,fb)
        thread_list.append(t)
    pbar.start()
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()
    fb.close()
    pbar.finish()
if __name__=='__main__':
    User_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
    url = "http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe"
    main(url,User_agent,5)




