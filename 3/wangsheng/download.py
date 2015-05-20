#!/usr/bin/env python
#Author:wangsh
#email:wangsheng219@163.com

import threading
import urllib2
import sys


max_thread =10

#初始化锁

lock = threading.RLock()


class Downloader(threading.Thread):
	def __init__(self,url,start_size,end_dize,fobj,buffer):
		self.url=url
		self.buffer=buffer
		self.start_size =start_size
		self.end_dize = end_size
		self.fobj = fobj
		threading.Thread.__init__(self)
	def run(self):

		with lock:
			print 'starting:%s'%self.getName()
	def __download(self)
		"""
			实际操作
		"""
		req = urllib2.Request(self.url)
		req.headers['Range']='bytes=%s-%s'(self.start_size,self.end_size)
		f=urllib2.urlopen(req)
		offset = self.start_size
		#一直循环下去？
		while 1:
			block = f.read(slef.buffer)
			#当前线程数据获取完毕后退出
			if not block:
				with lock:
					print '%s done'%self.getName()
					break
			with lock:
					sys.stdout.write('%s saveing block....'self.getName())
					#设置文件的便宜量
					self.fobj.seek(offset)
					#写入获取到的数据
					self.fobj.write(block)
					offset = offset+len(block)
					sys.stdout.write('done.\n')
def main(url,thread=3,save_file='',buffer=1024)
	#最大线程数量不能超过max_thread
	thread = thread if thread < max_thread else max_thread
	#获取文件大小
	req = urllib2.urlopen(url)
    size = int(req.info().getheaders('Content-Length')[0])
    # 初始化文件对象
    fobj = open(save_file, 'wb')
    # 根据线程数量计算 每个线程负责的http Range 大小
    avg_size, pad_size = divmod(size, thread)
    plist = []
    for i in xrange(thread):
        start_size = i*avg_size
        end_size = start_size + avg_size - 1
        if i == thread - 1:
            # 最后一个线程加上pad_size
            end_size = end_size + pad_size + 1
        t = Downloader(url, start_size, end_size, fobj, buffer)
        plist.append(t)
 
    #  开始搬砖
    for t in plist:
        t.start()
 
    # 等待所有线程结束
    for t in plist:
        t.join()
 
    # 结束当然记得关闭文件对象
    fobj.close()
    print 'Download completed!'
 
if __name__ == '__main__':
    url = 'http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
    main(url=url, thread=10, save_file='test.iso', buffer=4096)	

