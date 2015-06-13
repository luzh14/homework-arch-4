#!/usr/bin/env python
# coding=utf-8

import sys, os 
import MySQLdb as mysql
import json
import hashlib

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet


db = mysql.connect(user="root", passwd="", \
        db="lijulong", charset="utf8")
db.autocommit(True)
c = db.cursor()

def insertMonData(d_in):
    try:
        data = json.loads(d_in)
        print data

        sql = "INSERT INTO `stat_0` (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) VALUES('%s', '%d', '%d', '%d', '%s','%s', '%d')" % \
            (data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], data['StatsdCPUUse'],dTime)
        print sql
        ret = c.execute(sql)
    except mysql.IntegrityError:
        pass
    

if __name__ == '__main__':
    def logic(d_in):
        insertMonData(d_in)
#        print d_in
        return("OK")

    saverD = nbNet('0.0.0.0', 50251, logic)
    saverD.run()


