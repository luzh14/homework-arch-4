#!/usr/bin/env python
#encoding:utf8

import urllib2
import urllib
import random
from bs4 import BeautifulSoup

for num in range(10):

    url='http://www.dbmeizi.com/category/12?p=%s' % int(num)

    html = urllib2.urlopen(url).read()

    soup = BeautifulSoup(html)

    for i in  soup.find_all('div',attrs={"class": "img_con"}): 
        print(i.span.img.get('data-bigimg'))
        #file("%d.png" % i, "wb").write(urllib2.urlopen(i.span.img.get('data-bigimg')).read())
