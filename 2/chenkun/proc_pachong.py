#!/usr/bin/python  
#coding=utf-8

import re,time,urllib,urllib2,cookielib,multiprocessing
img_path="/opt/imgs/"

def down_imgs():
        url_login = 'http://www.douban.com/accounts/login'
        values = {'form_email':'chenkun0226@163.com','form_password':'abc12345678'}
        data = urllib.urlencode(values)
        headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        req = urllib2.Request(url_login, data,headers)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        the_page = response.read().decode("utf-8").encode("gbk")
        url_list = re.findall('"http://.*.jpg" alt',the_page)
        for url_u in url_list:
                img_url = url_u.split(' ')[0].strip('"')
                img_name = img_url.split('/')[-1]
                urllib.urlretrieve(img_url,img_path+img_name)
                print "%s saved!" %img_name

if __name__ == "__main__":
        pool = multiprocessing.Pool(processes=120)
        pool.apply_async(down_imgs,())
        time.sleep(0.2)

        pool.close()
        pool.join()
