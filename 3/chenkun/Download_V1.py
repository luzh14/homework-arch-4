#!/usr/bin/env python
# coding=utf-8
''' 单任务多线程下载:把要下载的文件"分段",每段启一个线程去下载 '''
 
import time,threading,urllib2,Queue
_lock = threading.Lock()
 
class Downloader(threading.Thread):
	def __init__(self, url, Save_File, buffer, queue):
        	self.url = url
        	self.buffer = buffer
        	self.Save_File = Save_File
		self.queue = queue
        	threading.Thread.__init__(self)
	def run(self):
		self.down_point = self.queue.get()
		self.start_size = self.down_point[0]
		self.end_size = self.down_point[1]
        	req = urllib2.Request(self.url)
        	req.headers['Range'] = 'bytes=%s-%s' % (self.start_size, self.end_size)
        	f = urllib2.urlopen(req)
        	offset = self.start_size
        	while True:
			with _lock:
                		block = f.read(self.buffer)
                		if block == '':break
                		self.Save_File.seek(offset)
                		self.Save_File.write(block)
                		offset = offset + len(block)
		print '%s down ok!' %self.name
		self.queue.task_done()

def Main(url, file_name, thread_num=3, buffer=1024):
	ck_queue = Queue.Queue()
	req = urllib2.urlopen(url)
	size = int(req.info().getheaders('Content-Length')[0])
	Save_File = open(file_name, 'wb')
	avg_size, pad_size = divmod(size, thread_num)

        for t in range(thread_num):
        	down_thd = Downloader(url,Save_File,buffer,ck_queue)
		down_thd.setDaemon(True)
		down_thd.start()
        for i in range(thread_num):
        	start_size = i*avg_size
        	end_size = start_size + avg_size - 1
        	if i == thread_num - 1:
                	end_size = end_size + pad_size
		ck_queue.put([start_size,end_size])
	ck_queue.join()	
	Save_File.close()
 
if __name__ == '__main__':
        u1 = 'http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
	url_list=[u1]
	for url in url_list:
		file_name = url.split('/')[-1]
		print 'Start Download %s' %file_name
		Main(url, file_name, thread_num=12, buffer=4096)

