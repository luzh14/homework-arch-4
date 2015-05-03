# -*- coding: utf-8 -*-
__author__ = 'luke'


from urllib2 import Request, urlopen, URLError, HTTPError
import urllib
import re
import os
def get_pics():
    data = {}
    data['cat']=1005
    data['q']='逗逼'
    print data
    url_values = urllib.urlencode(data)
    url = "http://www.douban.com/search"
    full_url = url + '?' + url_values
    print full_url
    req = Request(full_url)
    try:
        response = urlopen(req)
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        # everything is fine
    else:
        print 'No exception was raised.'
    html_result=response.read()
    #print  html_result
    pic_pattern=re.compile(r'\s*<img\ssrc="(.*)"\salt="(.*)">')
    url_list=re.findall(pic_pattern,html_result)
    return url_list

def save_pic(pic_list):
    path=r'./temp/'

    for pic in pic_list:
        name=pic[1].decode("utf-8")
        url=pic[0]
        file_name=name+'.jpg'   #文件名，包含文件格式
        dest_dir=os.path.join(path,file_name)
        try:
            urllib.urlretrieve(url , dest_dir)
        except:
            print '\tError retrieving the URL:', dest_dir


if __name__ == "__main__":
    pic_list=get_pics()
    save_pic(pic_list)
