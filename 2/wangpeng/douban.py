#!/usr/bin/env python
#coding=utf-8
import urllib2
import urllib
import os,re,sys

page_num = 1
while page_num < 100:
    url = "http://www.douban.com/interest/1/1/?p=%d" % page_num
    content = urllib2.urlopen(url).read()
    re_img = re.findall(r'img src="(.*)"\salt="(.*)"/></a>', content)
    page_num+=1
    for l in re_img:
        if not os.path.exists('db_imgs'):
            os.mkdir('db_imgs')
        img_url = l[0]
        img_head = urllib.urlopen(img_url).read()
        img_name = 'db_imgs'+'/'+l[1]+'.jpg'
        print img_name
        with open(img_name,'w') as f:
            f.write(img_head)
f.close()
