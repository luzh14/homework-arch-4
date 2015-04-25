#!/usr/bin/env  python
#coding:utf-8

import urllib2
import re
from bs4 import BeautifulSoup

class get_icon:
    def __init__(self):
        self.url = "http://www.douban.com"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'}

    def open_url(self):
        req = urllib2.Request(self.url, headers=self.headers)
        html = urllib2.urlopen(req).read()
        url_list = []
        soup = BeautifulSoup(html)
        for x in soup.find_all('a'):
            m = re.findall(r'http://[a-z]+.douban.com/.*',x['href'])
            if m:url_list.append(m[0])
        return url_list

    def save_img(self,num,args):
        icon_list = []
        for x in args:
            req = urllib2.Request(x, headers=self.headers)
            html = urllib2.urlopen(req).read()
            m = re.findall(r'http://img3.douban.com/icon/\w\d+-\d.jpg',html)
            if m:icon_list.append(m[0])
            if num == len(icon_list):break
        return icon_list

if __name__ == '__main__':
    x = get_icon()
    num = int(raw_input("\033[31m please input a num: \033[0m").strip())
    url_list = x.open_url()
    for l in x.save(num,url_list):
        name = re.findall(r'\w\d+-\d+.jpg',h)
        img = urllib2.urlopen(l).read()
        with open('/data/img/%s' %name,'w') as f:
            f.write(img)
