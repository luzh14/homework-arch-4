#!/usr/bin/env python
import urllib2 re
def GetHtml(url)
    html = urlib2.urlopen(url).read()
    return html
def GetImage(content)
    reg = re.compile("img3.douban.com/icon")
    results=re.findall(reg,content)
    return results
def SaveFile(results)
    filename=re.split(results)
    img=urlib2.urlopen(url)





if __name__=="__main__":
    html = get
