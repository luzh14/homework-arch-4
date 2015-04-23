#!/usr/bin/env python
# coding=utf-8
'''''
Created on 2015-04-22 14:51:39
@author: LiHongYuan
'''
import urllib2
import urllib
from bs4 import BeautifulSoup
import random
import time
import re
import sys   
reload(sys) # 解决字符集乱码问题，Python2.X以后初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8')


class DouUserPictureSpider:

    def __init__(self,url):
        print ("启动爬虫")
        print ("网页地址：" + url)
        #定义http agent请求头
        user_agent = [
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',  
                    'Opera/9.25 (Windows NT 5.1; U; en)',  
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',  
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',  
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',  
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',  
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",  
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
                      ]
        #print user_agent
        #随机选择useragent,并添加到header中
        agent = random.choice(user_agent)
        req = urllib2.Request(url)
        req.add_header('User-Agent', agent)
        req.add_header('Host','test.51reboot.com')
        req.add_header('Accept','*/*')
        req.add_header('Referer','http://www.google.com')
        req.add_header('GET',url)
        
        #获取请求页面的内容
        #html = urllib2.urlopen(url)
        html = self.urlProxies(url)
        self.page = html.read()
        
        #判断请求页面是否为空
        if self.page.strip == '':
            exit()
        else:

            pageContent = self.formatHtml(self.page)
            
            self.saveFile(pageContent)
            
    #定义代理地址，使用代理        
    def urlProxies(self,url):
        proxylist = (
            '211.167.112.14:80',
            '210.32.34.115:8080',
            '115.47.8.39:80',
            '211.151.181.41:80',
            '219.239.26.23:80',                         
        )
        for proxy in proxylist:
            proxies = {'': proxy}
            opener = urllib.FancyURLopener(proxies)
            f = opener.open(url)
            return f
    #定义打印信息
    def printInfo(self,filename):
        print(filename)
        print('图片标题是：'+ filename +'\n')
        print('图片已经存储成功！')
    
    #格式化网页格式    
    def formatHtml(self,page):
        htmlContent = BeautifulSoup(page)
        #print(htmlContent)
        return htmlContent  
    
    #获取下一页的地址
    def getNextPageUrl(self):
        page =self.formatHtml(self.page)
        nextPageUrl = page.find("div",class_="paginator").find("span",class_="next").find('a').get('href')
        return nextPageUrl
    
    #保存文件，并重命名
    def saveFile(self,page):
        path = "/xdfapp/scripts/picture/"
        for line in page.find_all("img"):
            imageUrl=line.get('src')
            #如果图片名字为None，生成一个随机数命名
            if line.get('alt') == None:
                
                name = '%d' %(random.randint(0,100002000)) + '.jpg'
            #    print(name)
            else:
                name = self.validateTitle(line.get('alt')) + '.jpg'
                    
            urllib.urlretrieve(imageUrl, path + name)
            self.printInfo(name)
        print('完成下载，即将开始下载'+self.getNextPageUrl()) 
        time.sleep(3)
       
    #去除文件名中的非法字符
    def validateTitle(self,name):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_name = re.sub(rstr, "", name)
        return new_name
#爬虫启动类           
class Scheduler:  
    def __init__(self,url):  
        self.start_url = url  
  
    def start(self):  
        spider = DouUserPictureSpider(self.start_url)  
        #print('进程开始、。。。。。。')  
        while True:  
            if spider.getNextPageUrl():  
                spider = DouUserPictureSpider(spider.getNextPageUrl())  
                print(spider.getNextPageUrl() + '即将开始下载。。。。') 
            elif spider.getNextPageUrl() == None:  
                print 'All article haved been downloaded!'  
                break   
            time.sleep(10)  
#开始的URL地址          
url = "http://www.douban.com/group/236951/members?start=0"   
Scheduler(url).start()
