#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import sendData_mh, nbNet

#saver_l = ['baidu.com:88','localhost:50001']
saver_l = ['localhost:50001']#,'baidu.com:88']
ff_l = ['localhost:50002']
saver_sock_l = [None]
ff_sock_l = [None]
def sendSaver(d_in,saver_l):
    return sendData_mh(saver_sock_l, saver_l, d_in)

def sendFf(d_in,saver_l):
    return sendData_mh(ff_sock_l, ff_l, d_in)

if __name__ == "__main__":
    def logic(d_in):
        ret_ff = sendFf(d_in, ff_l)
        ret_ss = sendSaver(d_in, saver_l)
        if ret_ss == "OK":
            print "SendSave OK"
            return("OK")
        else:
            return("SendSave Error")
    transD = nbNet('0.0.0.0', 50000, logic)
    transD.run()

