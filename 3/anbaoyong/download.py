#!/usr/bin/env python
#coding = utf-8
import threading
import sys
import urllib2
url=sys.argv[1]
thread_num=int(sys.argv[2])

 

file_size=int(urllib2.urlopen(url).info()['Content-Length'])
part_size=file_size / thread_num
last_size=(thread_num - 1)*part_size
Rangelist=[(str(x),str(x + part_size - 1)) for x in xrange(0,file_size,part_size) if x < last_size]

def download(size,f):
    head = {
    'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
    'Range':'bytes=%s' % size
    }
    req = urllib2.Request(url,headers=head)
    data = urllib2.urlopen(req).read()
    
   # threadlock.acquire()
    #with open('QQ.exe','w+') as f:
    f.seek(int(size.split('-')[0]))
    f.write(data)
    f.flush()
   # threadlock.release()


def setup():
    #threadlock = threading.Lock()
    threads = []
    file_fd = []
    for part in Rangelist:
        part = '%s-%s' % part
        file_fd.append(open('qq.exe','w+'))
        threads.append(threading.Thread(target=download,args=(part,file_fd.pop())))
    else:
        file_fd.append(open('qq.exe','w+'))
        threads.append(threading.Thread(target=download,args=(str(last_size)+'-',file_fd.pop())))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    setup()
