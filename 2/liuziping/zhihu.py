#!/usr/bin/env python
import re,sys
import urllib
def GetHtml(url):
	html = urllib.urlopen("http://www.zhihu.com")
	content = html.read()
	return content         
def GetImgs(content):
	reg = r'http://pic[0-9].*.jpg'
	compile = re.compile(reg)
	imgs=re.findall(compile,content)
	num=1
	for img in imgs:
		#return img        #debug
		urllib.urlretrieve(img,'%s.jpg' % num)  #the images name like  1.jpg 2.jpg
		num += 1
if __name__ == "__main__":
	html = GetHtml("http://www.zhihu.com")
	GetImgs(html)
