#/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
from bs4 import BeautifulSoup
from PIL import Image

url_template = "http://www.douban.com/online/12159983/participant?start=%s"

def get_content(page=0):
    url = url_template % page
    users = dict()
    content = urllib.urlopen(url).read()
    bs = BeautifulSoup(content)
    for item in bs.find_all("a"):
        if item.img != None:
            users[item.img['alt']] = item.img['src']
    return users

def img_resize(filename):
    im = Image.open(filename)
    im.thumbnail((32,32), Image.ANTIALIAS)
    im.save('thumbnail_'+filename)
    
def myspider():   
    for i in range(6):
        u_imgs = get_content(i*70)
        filename=""
        for item in u_imgs.items():
            file_suffix = item[1].split('.')[-1]        

            if item[0].count('*'):
                filename = item[0].strip("*")+'.'+file_suffix
            else:
                filename = item[0]+'.'+file_suffix

            tmp_file = open(filename, 'wb')
            img_content = urllib.urlopen(item[1]).read()
            tmp_file.write(img_content)
            tmp_file.close()
            img_resize(filename)

if __name__ == '__main__':
    myspider()
