#!/usr/bin/env python
# coding=utf-8

import sys, os 
import MySQLdb as mysql
import json
import hashlib

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet, sendData_mh

save_l = ["localhost:9650", "127.0.0.1:9650"]
ff_l = ["localhost:9652", "127.0.0.1:9652"]

saver_sock_l = [None]
ff_sock_l = [None]

def sendSaver(d_in, saver_l):
    return sendData_mh(saver_sock_l, saver_l, d_in)


def sendFf(d_in, saver_l):
    return sendData_mh(ff_sock_l, ff_l, d_in)


if __name__ == '__main__':
    def logic(d_in):
        sendFf(d_in, ff_l)
        ret = sendSaver(d_in, save_l)
        if ret:
            return("OK")
        else:
            return("ER")


        return("OK")

    transD = nbNet('0.0.0.0', 9651, logic)
    transD.run()


