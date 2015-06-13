#!/usr/bin/env python
# coding=utf-8

import sys, os 
import json
import hashlib

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet,sendData_mh
from ff import handle

sock_l = [None]
host_l = ['10.16.48.81:50001']

def transf(sock_l,host_l,data):
    return sendData_mh(sock_l,host_l,data)



if __name__ == '__main__':
    def logic(d_in):
        print d_in
        main(json.loads(d_in))
        transf(sock_l,host_l,d_in)
        return "OK"

    saverD = nbNet('0.0.0.0', 12888, logic)
    saverD.run()
