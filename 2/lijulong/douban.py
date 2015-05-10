#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'julong'
import os
import urllib
import urllib2
import time
import re
#<span class="fl p5 title">\s+<a title=".*href="(.*?)"
def getimage(number):
    ourdir=os.getcwd()
    imgdir=os.path.join(ourdir,'img')
    if not os.path.isdir(imgdir):
        os.mkdir(imgdir)
    #os.chdir(imgdir)
    count = 0
    userCount = 0
    while True:
        url = "http://www.dbmeizi.com/?p="+str(count)
        counter= urllib.urlopen(url).read()
        re_url=re.findall(r'<a title=".*\shref="(.*?)"',counter)
        for i in re_url:
            titleUrl="http://www.dbmeizi.com"+i
            #print titleUrl
            counterTitle=urllib.urlopen(titleUrl).read()
            source_url=re.findall(r'<a target="_blank" href="(.*?)">查看原帖',counterTitle)
            for sourcei in source_url:
                print sourcei
                source = urllib.urlopen(sourcei).read()
                #source = urllib.urlopen("http://www.douban.com/group/topic/74961854/").read()
                userimageDict=re.findall(r'<div class="user-face">\s*<a href=".*?"><img class="pil" src="(.*?)" alt.*',source)
                if userimageDict!=None and userimageDict != []:
                    userCount += 1
                    if userCount <= number:
                        userimage=userimageDict[0]
                        #print userimage
                        #print  userimageDict
                        username=re.findall(r'<div class="user-face">\s*<a href=".*?"><img class="pil" src=".*?" alt="(.*?)"',source)
                        Uusername=unicode(username[0],"utf-8")
                        #print Uusername
                        userimagedir=os.path.join(imgdir,Uusername)
                        if not os.path.isdir(userimagedir):
                            os.mkdir(userimagedir)
                        os.chdir(userimagedir)
                        continuer = urllib.urlopen(userimage).read()
                        user = open(Uusername+".jpg","wb+")
                        user.write(continuer)
                        user.close()
                        imgurl = re.findall(r'<div class="topic-figure cc">\s+<img src="(.*?)"',source)
                        if len(imgurl) >= 1 :
                            for img in imgurl:
                                file_name = urllib2.unquote(img).decode('utf8').split('/')[-1]
                                imgFileName = os.path.join(userimagedir,file_name)
                                if not os.path.exists(imgFileName):
                                    continuer = urllib.urlopen(img).read()
                                    user = open(file_name,"wb+")
                                    user.write(continuer)
                                    user.close()
                                    time.sleep(1)
                        else:
                            print "no data"
                    else:
                        break
        count += 1


if __name__=="__main__":
    print "test"
    getimage(100)
