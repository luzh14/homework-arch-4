#!/usr/bin/env python
#coding: utf8

import urllib
import re

def getHtml(url):
    html = urllib.urlopen(url)
    read = html.read()
    return read

def getImage(read):
    reg = r'src="(.*?\.jpg)"'
    #imgre = re.compile(reg)
    image = re.findall(reg,read)
    #return image

    x = 0
    for i in image:
        urllib.urlretrieve(i,'%s.jpg' % x)
        x+=1

read = getHtml('http://www.douban.com')
print getImage(read)
    
