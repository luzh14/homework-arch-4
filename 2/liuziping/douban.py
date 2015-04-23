#!/usr/bin/env python
#coding:utf8
'''
思路：豆瓣头像可以从用户的豆瓣账号入手，发现连接是http://www.douban.com/userid/, 可以随意找一个id段，从我自己的id 40128078开始往前数200个到40128278，这个段都是2010年左右注册的，活跃度不太高，好的都没有头像，有头像的话，头像的url是有规律的<img src="http://img3.douban.com/icon/u40128078-2.jpg" alt="且听风吟">， 地址直接是用我的id拼接的，没有头像的话，连接是默认的url，eg：<img src="http://img3.douban.com/icon/user_normal.jpg" alt="fangfang">
'''
import urllib,re

for uid in xrange(40128078,40128478)
	status=urllib.urlopen("http://www.douban.com/people/40128079/").getcode()   #返回状态不是200的都干掉，
