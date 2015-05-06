#!/usr/bin/env python
#coding=utf-8
'''
版本: 1.0
功能: 非登录状态，抓取豆瓣小组某个热门话题的用户头像
作者：liuziping
日期：2015-5-6
'''
import urllib
import re,sys,os

def GetImgs():
    if not os.path.exists('douban_imgs'):
        os.mkdir('douban_imgs')
        os.chdir('douban_imgs')
    for num in 0,100,200,300:
        url = "http://www.douban.com/group/topic/73873048/?start=%d" % num
        content = urllib.urlopen(url).read()
        #print content
        #sys.exit()
        imgs = re.findall(r'<img class="pil" src="(.*)" alt="(.*)"',content)
        #print imgs
        #sys.exit()
        for img in imgs:
            img_url = img[0]
            img_name = img[1]
            urllib.urlretrieve(img_url,"%s.jpg" % img_name)
if __name__ == "__main__":
    GetImgs()
