#!/usr/bin/env python
import urllib,urllib2
from bs4 import BeautifulSoup 
import re
meiziurl=[]
for page in [1,2,3]:
    urlpage=urllib2.urlopen('http://www.dbmeizi.com/?p=%s' %  page)  
    sou=BeautifulSoup(urlpage)
    #x=re.findall('http://.*?.jpg',sou)
    imgurl=sou.find_all('img')
    for i in imgurl:
        url=i.get('src')
        if  not url == None:
            meiziurl.append(url)


#for i in meiziurl:
#    print i
for i in meiziurl:
    with open(i.split('/')[-1],'w') as f:
            f.write(urllib2.urlopen(i).read())
