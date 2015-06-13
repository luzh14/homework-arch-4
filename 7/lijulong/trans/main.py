#!/usr/bin/env python
# coding=utf-8

import sys, os 
import MySQLdb as mysql
import json
import hashlib

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import sendData_mh
from simpleNet.nbNetFramework import nbNet

trans_l = ['baidu.com:8888','localhost:50251']
trans_ff = ['baidu.com:8888','localhost:50252']

sock_l = [None]
sock_ff = [None]
def sendSaver(d_in):
    return sendData_mh(sock_l,trans_l,d_in)

def sendFF(d_in):
    return sendData_mh(sock_ff,trans_ff,d_in)

if __name__ == '__main__':
    def logic(d_in):
#        print d_in
        while True:
            ret = sendSaver(d_in)
            #sendFF(d_in)
            if ret:
                return "OK"
            

    saverD = nbNet('0.0.0.0', 50250, logic)
    saverD.run()


