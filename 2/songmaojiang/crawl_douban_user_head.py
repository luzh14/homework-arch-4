#!/usr/bin/env python
# coding=utf8

from optparse import OptionParser
import sys

# from crawl and decompress html
import urllib
import urllib2
import socket 
import gzip
from StringIO import StringIO

import time
import random

# form web analysis/parsing
from pyquery import PyQuery as pq

pageNum = 30

socket.setdefaulttimeout(10)

accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
agent1 = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
agent2 = '(KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
agent = agent1 + ' ' + agent2



'''
check two argument for prog. -n=100 for default
'''
def checkArgv():
    global originUrl, maxNum

    usg = 'usage: \n\t%prog -u beginUrl -n maxNum'
    parser = OptionParser(usage=usg)
    parser.add_option('-u', '--url', dest = 'url',
            help="url of a douban user's followers for crawl", metavar='sring')
    parser.add_option('-n', '--max-num', dest = 'num', default=100, 
            help='max img numbers for crawl (100 for default)', metavar='int')
    (options, args) = parser.parse_args()
    
    try:
        maxNum = int(options.num)
    except ValueError:
        print('-n int should nonegative integer!')
        sys.exit(1)
    if options.url is None or maxNum < 1:
        parser.print_help()
        sys.exit(1)
    elif options.url.find('followers') == -1:
        print("ERROR:\n\t-u url should a douban user's followers")
        parser.print_help()
        sys.exit(1)

    originUrl = options.url



def crawlHtml(pUrl):
    req = urllib2.Request(pUrl)
    req.add_header('Accept', 'accept')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('User-Agent', agent)
    req.add_header('Cache-Control', 'max-age=0')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Accept-Language', 'en-US,en;q=0.8,zh;q=0.6,zh-CN;q=0.4')
    req.add_header('Referer', 'http://www.douban.com')
    req.add_header('DNT', '1')
    
    try:
        resp = urllib2.urlopen(req)
    except urllib2.URLError, reason:
        print(" + URLError when open url: %s, reason = %s" % (pUrl, reason))
    except urllib2.HTTPError, code:
        print(" + HTTPError when open url: %s, code = %s" % (pUrl, code))
    except:
        print(" + Unknown error when open url: %s" % pUrl)
        sys.exit(1)
    # 
    # decompress gzip
    if resp.info().get('Content-Encoding') == 'gzip':
        buff = StringIO(resp.read() )
        buff = gzip.GzipFile(fileobj=buff)
        html = buff.read()
    else:
        html = resp.read()

#    with open('test.html', 'w') as fp:
#        fp.write(html)
    return(html)


'''
give a html doc, parse the follower's logo image
return list of a dict with userName and imgUrl
'''
def parseUserLogoImg(pHtml):
    retList = []
    page = pq(pHtml)
    lists = page('ul.list-s li')
    for each in lists:
        url  = pq(each).find('div.pic a img').attr('src')
        name = pq(each).find('div.info span.name').text()
        if not url.endswith('user_normal.jpg'):
            retList.append( {'name': name, 'url': url} )
    return(retList)

'''
give a html doc, parse all the next pages url 
return a list of url
'''
def parseTotalNum(pHtml):
    page = pq(pHtml)
    h1 = page('div.main h1').text()
    h1 = h1.split('(')[1]
    return( int(h1[:len(h1)-1]) )


def timeSleep():
    interval = random.randint(5, 20)
    print('   Waiting %s seconds ...' % interval)
    time.sleep(interval)


'''
from userList, crawl each item, 
when crawl sucessed, add it in doneList
'''
def crawlUserImg(userList, doneList):
    for user in userList:
        print(user)
        html = crawlHtml(pUrl=user['url'])
        storeName = 'user_' + user['name'] + '.jpg'
        with open(storeName, 'wb') as fd:
            fd.write(html)
        doneList.append( user['name'] )
        timeSleep()


if __name__ == '__main__':
    '''
    Crawl user's head image with 48x48 pixels in www.douban.com.
    you should give two argvs: begin_url, and max uers(100 for default)
        begin_url should a user's followers such as:
        http://site.douban.com/vanessa/followers/
    '''
    checkArgv()
    userList = []
    doneList = []

    print('max num: %d' % maxNum)
    # crawl origin url
    html = crawlHtml(pUrl=originUrl)
    fp = open('test.html', 'r')
    html = fp.read().decode('utf-8')

    # analysis html and follow it
    userList.extend( parseUserLogoImg(html) )
    
    totalNum = parseTotalNum(html)
    pages = totalNum / pageNum + 1
    print(totalNum)
    print(pages)

    crawlUserImg(userList, doneList)

    # follow it 
    pageId = 1 
    while len(doneList) < maxNum:
        url = originUrl + '/?start=' + str(pageId * pageNum)
        print('-- url: %s' % url)
        html = crawlHtml(pUrl=url)
        userList = parseUserLogoImg(html)
        crawlUserImg(userList, doneList)
        pageId += 1
        if pageId <= pages:
            continue
        else:
            break

        
