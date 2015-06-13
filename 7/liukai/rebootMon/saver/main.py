#!/usr/bin/env python
# coding=utf-8

import sys, os 
import MySQLdb as mysql
import json
import hashlib

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet

monTables = [
    'stat_0',
    'stat_1',
    'stat_2',
    'stat_3',
]

db = mysql.connect(user="reboot", passwd="reboot123", \
        db="liukai", charset="utf8")
db.autocommit(True)
c = db.cursor()

def fnvhash(string):
    ret = 97
    for i in string:
        ret = ret ^ ord(i) * 13
    return ret

def insertMonData(d_in):
    try:
        data = json.loads(d_in)
        print data
        dTime = int(data['Time'])
        hostIndex = monTables[fnvhash(data['Host']) % len(monTables)]
        sql = "INSERT INTO `%s` (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) VALUES('%s', '%d', '%d', '%d', '%s', '%d')" % \
            (hostIndex, data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], dTime)
        ret = c.execute(sql)
    except mysql.IntegrityError:
        pass
    

if __name__ == '__main__':
    def logic(d_in):
        insertMonData(d_in)
#        print d_in
        return("OK")

    saverD = nbNet('0.0.0.0', 50136, logic)
    saverD.run()


