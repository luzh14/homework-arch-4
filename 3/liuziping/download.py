#!/usr/bin/env python
#coding:utf8

import urllib2

url="http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe"
def get_file_size(url):
    opener = urllib2.build_opener()
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        response = opener.open(request)
        response.read()
    except Exception, e:
        print '%s %s' % (url, e)
    else:
        return dict(response.headers).get('content-length', 0)
def download(url,start_size):
    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes=%d-%d'%(start_size,end_size)
    f = urllib2.urlopen(req)
    offset = start_size



if __name__ == '__main__':
    num =  get_file_size(url)
    print num
    
