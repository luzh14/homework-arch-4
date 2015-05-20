#!/usr/bin/env python
#Author:wangsh
#email:wangsheng219@163.com

import threading
import urllib2
import sys


max_thread =10

#��ʼ����

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
			ʵ�ʲ���
		"""
		req = urllib2.Request(self.url)
		req.headers['Range']='bytes=%s-%s'(self.start_size,self.end_size)
		f=urllib2.urlopen(req)
		offset = self.start_size
		#һֱѭ����ȥ��
		while 1:
			block = f.read(slef.buffer)
			#��ǰ�߳����ݻ�ȡ��Ϻ��˳�
			if not block:
				with lock:
					print '%s done'%self.getName()
					break
			with lock:
					sys.stdout.write('%s saveing block....'self.getName())
					#�����ļ��ı�����
					self.fobj.seek(offset)
					#д���ȡ��������
					self.fobj.write(block)
					offset = offset+len(block)
					sys.stdout.write('done.\n')
def main(url,thread=3,save_file='',buffer=1024)
	#����߳��������ܳ���max_thread
	thread = thread if thread < max_thread else max_thread
	#��ȡ�ļ���С
	req = urllib2.urlopen(url)
    size = int(req.info().getheaders('Content-Length')[0])
    # ��ʼ���ļ�����
    fobj = open(save_file, 'wb')
    # �����߳��������� ÿ���̸߳����http Range ��С
    avg_size, pad_size = divmod(size, thread)
    plist = []
    for i in xrange(thread):
        start_size = i*avg_size
        end_size = start_size + avg_size - 1
        if i == thread - 1:
            # ���һ���̼߳���pad_size
            end_size = end_size + pad_size + 1
        t = Downloader(url, start_size, end_size, fobj, buffer)
        plist.append(t)
 
    #  ��ʼ��ש
    for t in plist:
        t.start()
 
    # �ȴ������߳̽���
    for t in plist:
        t.join()
 
    # ������Ȼ�ǵùر��ļ�����
    fobj.close()
    print 'Download completed!'
 
if __name__ == '__main__':
    url = 'http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe'
    main(url=url, thread=10, save_file='test.iso', buffer=4096)	

