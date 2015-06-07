#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
author:      kakaxi
version:     0.2
create_time: 2015/05/14
"""
import requests
import threading
from threading import Lock

class FileMultiDownload(object):
    """ file multi thread downlaod """

    def __init__(self, url, filename=None, threadnum=None):
        self.url = url
        if not filename:
            self.filename = url.split("/")[-1]
        else:
            self.filename = filename
        
        if not threadnum:
            self.threadnum = 10
        else:
            self.threadnum = threadnum

        self.filesize = self.getFileSize()
        self.lock = Lock()
        self.fd = open(self.filename, 'w')

    def getFileSize(self):
        head_req = requests.head(self.url)
        filesize = int(head_req.headers.get("content-length", 0))
        return filesize


    def getSplitRange(self):
        """split the filesize by threadnum """
        step = self.filesize / self.threadnum
        lastbytes = self.filesize % self.threadnum
        ranges = [[i, i+step-1] for i in range(0, self.filesize, step)]
        if lastbytes != 0:
            ranges[-1][-1] = self.filesize - 1
        return ranges

    def downSplitFile(self,*range):
        """ 
        make range request
        and download the split
        """
        range_str = "bytes=%s-%s" % range
        headers = {'Range':range_str}
        req = requests.get(self.url, headers=headers)
        self.saveSplitToFile(req.content, range);
    
    def saveSplitToFile(self, content, range):
        """
        save split file to disk file
        """
        try:
            self.lock.acquire()
            self.fd.seek(range[0])
            self.fd.write(content)
            self.fd.flush()
        except Exception as e:
            print e
        finally:
            self.lock.release()


    def saveAllToFile(self):
        """
        download all split file 
        then save all split to one file
        """
        ranges = self.getSplitRange()
        thread_list = []
        for i in range(0, self.threadnum):
            t = threading.Thread(target=self.downSplitFile, args=ranges[i])
            t.start()
            thread_list.append(t)

        for t in thread_list:
            t.join()
        self.fd.close()



if __name__ == '__main__':
    url = "http://dldir1.qq.com/qqfile/qq/QQ7.1/14522/QQ7.1.exe"
    download = FileMultiDownload(url)
    download.saveAllToFile()
