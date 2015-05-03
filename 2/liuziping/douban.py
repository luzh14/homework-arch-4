#!/usr/bin/env python
#coding:utf8
'''
思路：豆瓣头像可以从用户的豆瓣账号入手，发现连接是http://www.douban.com/userid/, 可以随意找一个id段，从我自己的id 40128078开始往前数400个到40128478，这个段都是2010年左右注册的，活跃度不太高，好的都没有头像，有头像的话，头像的url是有规律的<img src="http://img3.douban.com/icon/u40128078-2.jpg" alt="且听风吟">， 地址直接是用我的id拼接的，没有头像的话，连接是默认的url，eg：<img src="http://img3.douban.com/icon/user_normal.jpg" alt="fangfang">
'''
import urllib,re,sys

num=0
s="200"
for uid in xrange(40128070,50128470):
	status=str(urllib.urlopen("http://www.douban.com/people/uid/").getcode())#返回状态不是200的说明用户被注销，干掉，
	if statusi == s:
		print uid
		num +=1
		print num
		if num == 10:
			print "ok"
			sys.exit()
	else:
		print "%s is null" % uid
