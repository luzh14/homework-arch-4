import urllib,urllib2
import re
import time
import threading
def furl():
  num = 0
  urllist = []
  while num <5:
    url='http://www.dbmeizi.com/?p=%d' % num
    urllist.append(url)
    num += 1
  return urllist

def meizi_url(url):
  res = urllib.urlopen(url).read()
  #meizi = re.findall(r'http://pic.dbmeizi.com.*.jpg',res)
  meizi = re.findall(r'src="(\w+://pic.dbmeizi.com/\w+/\w+/\w+/s_p\w+.jpg)"',res)
  return meizi


def get_meizi(meiziurl):
  res = urllib.urlopen(meiziurl).read()
  filename = meiziurl[-8:]
  with open(filename,'w') as f:
    f.write(res)
  

if __name__ == '__main__':
  stime = time.time()
  threads = []
  for url in furl():
    for x in meizi_url(url):
      threads.append(threading.Thread(target=get_meizi,args=(x,)))
  for t in threads:
    t.start()
  etime = time.time()
  print etime - stime
