#!/usr/bin/env python
import urllib2
import os,time,sys
import sys, getopt
import threading

def get_args():
    url = None
    thread_num = 1 
    usage = sys.argv[0] + ' -u URL -n thread_num'
    opts, args = getopt.getopt(sys.argv[1:], "hu:n:", ["help", "url=", "thread_num="])
    if opts:
        for op, value in opts:
            if op == '-u' or op == '--url':
                url = value
            elif op == '-n' or op == '--thread_num':
                thread_num = int(value)
            elif op == '-h':
                print usage 
                sys.exit(0)
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
    lst = []
    step = size / th_num
    L = [ step * i for i in xrange(0,th_num) ]
    for i in xrange(len(L)-1):
        lst.append([L[i],L[i+1]-1])
    lst.append([L[-1],size-1])
        #lst.append("%d-%d" % (L[i],L[i+1]-1))
    #lst.append("%d-%d" % (L[-1],size-1))
    return lst
    
def down_file(url,filename,span_list):
    response = urllib2.Request(url) 
#   response.add_header('Range', 'bytes=%d-%d' % (span_list[0],span_list[1]))
    response.add_header('Range','bytes={0[0]}-{0[1]}'.format(span_list))
    r = urllib2.urlopen(response)
    context = r.read()
    f = open(filename,'wb')
    f.write(context)
    f.close()

def combine_file(filename, tmp_f_list):
    filehandle = open(filename, 'wb+')
    for i in tmp_f_list:
        f = open(i, 'rb')
        filehandle.write(f.read())
        f.close()
        try:
            os.remove(i)
            print "moved", i
        except:
            print "xxxx" 

    filehandle.close()

def main():
    url, thread_num = get_args() 
    if not url or not thread_num:
        print "not available args."
        sys.exit(1)
    #url='http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
    filename=url.split('/')[-1] #'file.download'
    tmp_filename='.'+filename
    tmp_f_list = [ tmp_filename+str(x) for x in xrange(thread_num)]
    size = get_size(url)
    span_list = get_thread_list(size, thread_num)
    for i in xrange(thread_num):
        t = threading.Thread(target=down_file,args=(url,tmp_f_list[i],span_list[i]),)
        t.start()
    print "current has %d threads" % (threading.activeCount() - 1)
    while threading.activeCount(): 
        if threading.activeCount() == 1:
            combine_file(filename, tmp_f_list)
            print "current has %d threads" % (threading.activeCount() - 1)
            break
        else:
            pass

if __name__ == '__main__':
    main()
