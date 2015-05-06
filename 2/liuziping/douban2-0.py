#!/usr/bin/env python
#coding:utf8
'''
版本：2.0
功能：通过request或者cookie模拟登陆，然后抓取需要登陆页面的用户头像信息
思路：1:豆瓣头像可以从用户的豆瓣账号入手，发现连接是http://www.douban.com/userid/, 可以随意找一个id段，从我自己的id 40128078开始往前数400个到40128478，这个段都是2010年左右注册的，活跃度不太高，好的都没有头像，有头像的话，头像的url是有规律的<img src="http://img3.douban.com/icon/u40128078-2.jpg" alt="且听风吟">， 地址直接是用我的id拼接的，没有头像的话连接是默认的url，eg：<img src="http://img3.douban.com/icon/user_normal.jpg" alt="fangfang">
      2:找一个用户用户的关注成员页面,例如阿北关注的人http://www.douban.com/people/ahbei/contacts,正则匹配图片即可
作者：liuziping
日期：2015-05-06
备注：两个思路试了下，第一种比较费劲，很多用户都注销了，而第二种思想好很多，关注的成员至少是存在的
问题：如果已知某个用户的cookie，如何用已有的cookie模拟登陆，request提交暴露账户密码很恶心
'''
from urllib import urlencode
import cookielib, urllib2,urllib
import os,re,sys
def login():
    headers={'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9'}
    values = {'form_email':'787696331@qq.com','form_password':'douban2014','remember':1,'source':'simple','redir':'http://www.douban.com'}
    loginUrl = 'https://www.douban.com/accounts/login'
    data = urllib.urlencode(values)
    cookiejar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    urllib2.install_opener(opener)
    request = urllib2.Request(loginUrl ,data ,headers)
    result = urllib2.urlopen(request)
    login_result = result.read()
    if(login_result.find('/accounts/logout')): #如果代理里面有logout，说明已经登陆成功，可以干坏事了
        GetImg()
    else :
        print 'login faild'
def GetImg():
    if not os.path.exists('douban2_imgs'):
        os.mkdir('douban2_imgs')
        os.chdir('douban2_imgs')
    url = "http://www.douban.com/people/ahbei/contacts"
    html = urllib2.urlopen(url)
    content = html.read()
    imgs = re.findall(r'<img src="(.*\.jpg)" class="m_sub_img" alt="(.*)"',content)
    #<img src="http://img3.douban.com/icon/u49312430-1.jpg" class="m_sub_img" alt="金犁">   正则匹配的图片样式
    #print imgs
    #sys.exit()
    for img in imgs:
        img_url = img[0]
        img_name = img[1]
        urllib.urlretrieve(img_url,"%s.jpg" % img_name)
if __name__=='__main__':
    login()
