#!/usr/bin/env python
#encoding:utf8
import urllib2
import threading


class myThread(threading.Thread):

    def __init__(self, url_file, scope, url):
        threading.Thread.__init__(self)
        self.url_file = url_file
        self.scope = scope
        self.url = url

    def run(self):

        req_header = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
        'Accept':'text/html;q=0.9,*/*;q=0.8',
        'Range':'bytes=%s' % self.scope,
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Connection':'close',
        }
        
        req = urllib2.Request(self.url, headers=req_header)
        data = urllib2.urlopen(req, data=None).read()
        start_value = int(self.scope.split('-')[0])
        
        threadLock.acquire()

        self.url_file.seek(start_value)
        self.url_file.write(data)
        self.url_file.flush()
        threadLock.release()

if __name__ == '__main__':

    url = 'http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
    size=int(urllib2.urlopen(url).info()['content-length'])
    print size
    threadnum = 4
    len = size / (threadnum - 1)
    current = 0

    url_file = file(url.split('/')[-1],'wb+')
    threadLock = threading.Lock()
    threads = []
    for tName in range(1, threadnum + 1):
    
        if tName < threadnum:
            scope = "%d-%d" %(current,len * tName - 1)
            current = len * tName
        elif tName == threadnum:
            if current != size:
                scope = "%d-%d" %(current,size)
            else:
                scope = "%d-" %(current - 1)
        print scope
        thread = myThread(url_file, scope, url)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    url_file.flush()
    url_file.close()
    
    
    
