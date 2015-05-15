#!/usr/bin/env python
# coding=utf-8
''' 多任务多线程下载:同时启多个线程下载多个文件,并且把每个文件"分段",每段再启一个线程去下载 '''
 
import time,threading,urllib2,Queue
_lock = threading.Lock()
 
class Downloader(threading.Thread):
	def __init__(self, url, Save_F, buffer, queue):
        	self.url = url
        	self.buffer = buffer
        	self.Save_F = Save_F
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
                		self.Save_F.seek(offset)
                		self.Save_F.write(block)
                		offset = offset + len(block)
		print '%s down ok!' %self.name
		time.sleep(1)
		self.queue.task_done()

class init_thread(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.num_threads = 12
		self.url_queue = queue
		self.Downpoint_queue = Queue.Queue()
		self.buffer = 3072
	def run(self):
		while True:
			url = self.url_queue.get()
			file_name = url.split('/')[-1]
			print 'Start Download: %s' %(file_name)
			req = urllib2.urlopen(url)
			size = int(req.info().getheaders('Content-Length')[0])
			Save_F = open(file_name, 'wb')
			avg_size, pad_size = divmod(size, self.num_threads)

			for t in range(self.num_threads):
				Down_thd = Downloader(url, Save_F, self.buffer, self.Downpoint_queue)
				Down_thd.setDaemon(True)
				Down_thd.start()
			for i in range(self.num_threads):
				start_size = i*avg_size
				end_size = start_size + avg_size - 1
				if i == self.num_threads - 1:
					end_size = end_size + pad_size +1
				self.Downpoint_queue.put([start_size,end_size])
			self.Downpoint_queue.join()
			Save_F.close()
			self.url_queue.task_done()
			time.sleep(1)

if __name__ == '__main__':
	Threads = 3
	ck_queue = Queue.Queue()

        u1 = 'http://downmini.kugou.com/kugou7695.exe'
        u2 = 'http://dldir1.qq.com/weixin/Windows/WeChat1.1.exe'
        u3 = 'http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
	u4 = 'http://yydl.duowan.com/4/setup/YYSetup-7.5.0.0-zh-CN.exe'
	u5 = 'http://dl.liebao.cn/kb/KSbrowser_5.2.91.10096.exe'
	url_list=[u1,u2,u3,u4,u5]

        for T in range(Threads):
                init_thd = init_thread(ck_queue)
                init_thd.setDaemon(True)
                init_thd.start()
        for file_url in url_list:
                ck_queue.put(file_url)
        ck_queue.join()

