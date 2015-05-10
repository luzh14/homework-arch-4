# -*- coding: utf-8 -*-
__author__ = 'luke'


from urllib2 import Request, urlopen, URLError, HTTPError
import urllib
import re
import os
#获取豆瓣用户的头像图片的url和用户名，输出为一个列表，元素为元组，每个元组第一个元素是url第二个是用户名。
#获取方法是通过搜索关键字相关的用户，通过搜索结果页抓取用户头像
def get_pics():
    i=20
    n=0
    query_string={}
    query_string['cat']=1005
    query_string['q']='妹子'
    url_list=[]
    #由于豆瓣的搜索结果一次返回20个，需要循环抓取用户，用户数量为5×20，由于没有排重，用户名相同会被覆盖。
    while n<5:
        query_string['start']=i*n
        url_query = urllib.urlencode(query_string)
        add_imgcount_url = "http://www.douban.com/j/search" + '?' + url_query
        n=n+1
        add_imgcount_reg=Request(add_imgcount_url)
        try:
            resp=urlopen(add_imgcount_reg)
        except HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError, e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        # everything is fine
        else:
            print 'No exception was raised.'

        result=resp.read()
        patt=re.compile(r'\s*<img\ssrc=\\"(.*?\.jpg)\\"\salt=\\"(.*?)\\">')
        url_list.extend(re.findall(patt,result))
    return url_list

#将图片存到本地./temp/目录下，输入为get_pics()的输出
def save_pic(pic_list):
    path=r'./temp/'
    for pic in pic_list:
        name=pic[1].decode("utf-8")
        url=pic[0].replace('\\','')
        file_name=name+'.jpg'   #文件名，包含文件格式
        dest_dir=os.path.join(path,file_name)
        try:
            urllib.urlretrieve(url , dest_dir)
        except :
            print '\tError retrieving the URL:', dest_dir
            print


if __name__ == "__main__":
    pic_list=get_pics()
    save_pic(pic_list)
