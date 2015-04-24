# -*- coding: utf-8 -*-
import urllib
from HTMLParser import HTMLParser 
from PIL import Image
import os

class MyHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            if len(attrs) == 3:
                src=attrs[0]
                alt = attrs[-1]
                if src[0]=='src':
                    img_url=src[-1]
                if alt[0]=='alt':
                    user1 = alt[-1]
                    user = unicode(user1,'utf-8')
                self.img_define(img_url,user)      
    def img_define(self,url,user):
        img_tmp=u'D:\download_img\%s_tmp.jpg' %user
        img=u'D:\download_img\%s.jpg' %user
        with open(img_tmp,'wb') as img_file:
            img_file.write(urllib.urlopen(url).read())
        img_f = Image.open(img_tmp)
        out = img_f.resize((32,32),Image.ANTIALIAS)
        out.save(img)
        os.remove(img_tmp)
if __name__ == '__main__':
    url = 'http://www.douban.com/group/Ijob/members?start=0'
    content = urllib.urlopen(url).read()
    my = MyHtmlParser()
    my.feed(content)
    my.close()
