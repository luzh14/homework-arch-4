#!/usr/bin/env python
# coding=utf-8

import sys, os 
import json
import hashlib
#import MySQLdb as mysql

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet
import mailf


def insertMonData(d_in):
    data = json.loads(d_in)
        #data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], dTime
    if int(data['MemUsage']) > 1900 :
        mailf.mailf('%s MemUsage >1900'%data['Host'],'%s MemUsage is %s '% (data['Host'],data['MemUsage']))
    if   float(data['LoadAvg']) > 0.1 :
        mailf.mailf('LoadAvg is % '% data['LoadAvg'],'LoadAvg too high')        

if __name__ == '__main__':
    def logic(d_in):
        insertMonData(d_in)
#        print d_in
        return("OK")

    saverD = nbNet('0.0.0.0', 50002, logic)
    saverD.run()


