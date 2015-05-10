#coding=utf-8

import re
import time
import urllib
import urllib2

def douban_img(url, datadir, number):
    count = 0
    url_re = re.compile('(\w+://\w+.*/\w)(\d+)')
    name_re =re.compile('("username"> )(.+)( <)')
    imgurl= url_re.search(url).group(1)
    uid = int(url_re.search(url).group(2))
    hds = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
    while True:
        geturl = imgurl+str(uid)+'.jpg'
        getreq = urllib2.Request(geturl,headers=hds)
        try:
            urlres = urllib2.urlopen(getreq,timeout=3)
        except Exception,e:
            uid += 1
            continue
        nameurl= 'http://book.douban.com/people/' + str(uid)
        namereq= urllib2.Request(nameurl,headers=hds)
        nameres = urllib2.urlopen(namereq,timeout=3)
        namepage = nameres.read()
        name = name_re.search(namepage).group(2)
        urllib.urlretrieve(geturl, filename=datadir + name + '.jpg')
        count += 1
        if count == int(number):
            break
        uid += 1
        time.sleep(3)

if __name__ == "__main__":
    import os
    os_dir = os.getcwd()
    down_dir = os.path.join(os_dir, 'douban_download/')
    if not os.path.exists(down_dir):
            os.mkdir(down_dir)
    url = 'http://img3.douban.com/icon/u51391794-4.jpg'
    douban_img(url, down_dir, 100)
