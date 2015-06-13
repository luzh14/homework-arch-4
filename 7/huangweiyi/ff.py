#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys, os
import json
import threading

from conf import ff_conf
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet

def compare(data, conf):
    item, condation, value, mail = conf
    if data[item] < value:
        print "[%s]: %s lt %s" %(item, data[item], value)
        return True
    else:
        toMail(mail)
        return False

def toMail(mail):
    print "alarm %s" % mail


def ff(data, ff_conf):
    data = json.loads(data)
    th_array = []
    for conf in ff_conf:
        t = threading.Thread(target=compare, args=(data, conf,))
        th_array.append(t)
    for t in th_array:
        t.start()
    return True

if __name__ == '__main__':
    def logic(da_in):
        ret = ff(da_in, ff_conf)
        if ret:
            return "OK"
        else:
            return "ER"

    ffD = nbNet('0.0.0.0', 50000, logic)
    ffD.run()



