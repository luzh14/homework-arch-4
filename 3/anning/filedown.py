#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import division
import urllib2, sys, os, time
from threading import Thread, Lock
from progressbar import * 


class ProgressBar(object):

    """ Progress Bar for FileMuldown """

    sum = 0 
    lock=Lock()
    w=['Progress: ', Percentage(), ' ', Bar(marker='#',left='[', right=']'),' ', ETA(), ' ', FileTransferSpeed()]
    pbar=ProgressBar(widgets=w, maxval=100).start()
 
    @staticmethod
    def Barhandle((step,filesize)):
        with ProgressBar.lock:
            ProgressBar.sum += step
            per = ProgressBar.sum/filesize * 100.0
            ProgressBar.pbar.update(int(per))
            time.sleep(0.5)
 
    @staticmethod
    def callback(fun):
        def f(*args, **kw):
            ProgressBar.Barhandle(fun(*args, **kw))
        return f

class FileMuldown(ProgressBar):

    """ FileMuldown """

    @property
    def threadnum(self):
        return self._threadnum

    @threadnum.setter
    def threadnum(self, value):
        try:
            value = int(value)
        except (ValueError,TypeError):
            raise ValueError('threadnum must be an integer!')
        self._threadnum = value 

    @property
    def url(self):
        return self._url
 
    @url.setter
    def url(self, value):
        if not value.startswith('http://'):
            raise ValueError('url must be an web addr!')
        self._url = value

    def run(self):
        threadlist = []
        self.filesize = int(self.fileinfo())
        arglist = self.__threadAllocation()

        self.filename = self._url.split('/')[-1]
        os.mknod(self.filename)

        for i in xrange(len(arglist)):
            t = Thread(target=self.threadHandle, args=arglist[i])
            t.start()
            threadlist.append(t)

        for i in threadlist:
            i.join()

    def __threadAllocation(self):
        offerset, remainder = divmod(self.filesize,self._threadnum)
        arglist = [(offerset*i,offerset*(i+1)-1) for i in xrange(self._threadnum)]
        modifiA, modifiB = arglist[-1]
        arglist[-1] = modifiA, modifiB+remainder 
        return arglist

    def fileinfo(self):
        request = urllib2.Request(self._url)
        response = urllib2.urlopen(request)
        infos = response.headers.dict
        return infos.get('content-length')

    @ProgressBar.callback
    def threadHandle(self, startpos, endpos):
        request = urllib2.Request(self._url)
        request.headers['Range'] = 'bytes=%s-%s' % (startpos, endpos)
        response = urllib2.urlopen(request)
        text = response.read()

        with file(self.filename,'rb+') as f:
            f.seek(startpos)
            f.write(text)
        step = endpos-startpos+1
        return step,self.filesize


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'You enter the parameter is not correct.'
        sys.exit()

    filedown = FileMuldown()
    filedown.url = sys.argv[1]
    filedown.threadnum = sys.argv[2]
    filedown.run()
    print '\n\n下载完成 !!!!!!\n'


