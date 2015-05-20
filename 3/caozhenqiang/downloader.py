#!/usr/bin/env python
import urllib2
import os,sys
import sys, getopt
import threading

def get_args():
    url = None
    thread_num = 1 
    usage = sys.argv[0] + ' -u URL -n thread_num'
    opts, args = getopt.getopt(sys.argv[1:], "hu:n:", ["help", "url=", "thread_num="])
    if opts:
        for op, value in opts:
            if op == '-u': 
                url = value
            elif op == '-n': 
                thread_num = int(value)
            else:
                print usage
                sys.exit(1)
    else:
        print usage
        sys.exit(2)
    return url, thread_num

def get_size(url):
    opener = urllib2.build_opener()
    req = opener.open(url)
    meta = req.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    return file_size

def get_thread_list(size,th_num):
    step = size / th_num
    lst=[[step * i, step * (i + 1) - 1] for i in xrange(0,th_num-1)]
    lst.append([step*(i+1) - 1, size])
    return lst
    
def down_file(url,fd,Range_list):
    response = urllib2.Request(url) 
#   response.add_header('Range', 'bytes=%d-%d' % (Range_list[0],Range_list[1]))
    response.add_header('Range','bytes={0[0]}-{0[1]}'.format(Range_list))
    r = urllib2.urlopen(response)
    context = r.read()
    f = fd
    print f
    f.seek(Range_list[0])
    f.write(context)

def main():
    url, thread_num = get_args() 
    filename=url.split('/')[-1] #'file.download'
    filesize = get_size(url)
    Range_list = get_thread_list(filesize, thread_num)

    fd = []
    for i in xrange(thread_num):
        fd.append(open(filename,'w+'))
        t = threading.Thread(target=down_file,args=(url,fd.pop(),Range_list[i]),)
        print "Range_list %d: " % i , Range_list[i]
        t.start()
    print "Currently, there are %d child threads" % (threading.activeCount() - 1)

if __name__ == '__main__':
    main()
