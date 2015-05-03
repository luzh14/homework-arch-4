# -*- coding: utf-8 -*-
__author__ = 'luke'


from urllib2 import Request, urlopen, URLError, HTTPError
import urllib
import re
def get_head_pic():
    data = {}
    data['cat']=1005
    data['q']='妹子'
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
    html_result=response.read().decode("utf-8")
    print  html_result
    pattern=re.compile(r'\s*<img\ssrc="(.*)"\salt="(.*)">')
    match1=pattern.match(html_result)
    print match1.group()

get_head_pic()