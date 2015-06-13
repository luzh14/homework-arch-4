#!/usr/bin/python
import Queue
import threading
import time
import json
import urllib2
import socket
import commands
import pdb
from moniItems import mon

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import sendData_mh

trans_l = ['127.0.0.1:50137', 'localhost:50137']

class porterThread (threading.Thread):
    def __init__(self, name, q, ql=None, interval=None):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
        #self.queueLock = ql
        self.interval = interval
        self.sock_l = [None]

    def run(self):
        #print "Starting %s"  % self.name
        if self.name == 'collect':
            self.put_data()
        elif self.name == 'sendjson':
            self.get_data()

    def put_data(self):
        m = mon()
        atime=int(time.time())
        while 1:
            data = m.runAllGet()
            #print data 
            #self.queueLock.acquire()
            self.q.put(data)
            #self.queueLock.release()
            btime=int(time.time())
            #print '%s  %s' % (str(data), self.interval-((btime-atime)%30))
            time.sleep(self.interval-((btime-atime)%self.interval))
            
    def get_data(self):
        while 1:
            print "get"
            #self.queueLock.acquire()
            if not self.q.empty():
                data = self.q.get()
                print data
                #pdb.set_trace()
                sendData_mh(self.sock_l, trans_l, json.dumps(data))
            #self.queueLock.release()
            time.sleep(self.interval)

def startTh():
    q1 = Queue.Queue(10)
    ql1 = threading.Lock()
    collect = porterThread('collect', q1, ql1, interval=3)
    collect.start()
    time.sleep(0.5)
    sendjson = porterThread('sendjson', q1, ql1, interval=3)
    sendjson.start()
    q2 = Queue.Queue(10)
    print  "start"
    collect.join()
    sendjson.join()
if __name__ == "__main__":
    startTh()


