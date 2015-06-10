#!/usr/bin/env python
# coding=utf-8
import MySQLdb as mysql
import sys, os 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet
import json,hashlib

monTables = [
    'stat_0',
    'stat_1',
    'stat_2',
    'stat_3',
]

conn = mysql.connect(user = 'root', db='reboot', charset = 'utf8')
conn.autocommit(True)
c =conn.cursor()

def logic(d_in):
    try:
        data  = json.loads(d_in)
        print data
        dTime = int(data['Time'])
        hostHash = hashlib.md5()
        hostHash.update(data['Host'])
        hostIndex = monTables[ord(hostHash.digest()[-1]) % len(monTables)]
        sql = "insert into %s (host,mem_free,mem_usage,mem_total,load_avg,time) values ('%s',%d,%d,%d,'%s',%d)" %\
            (hostIndex,data['Host'],data['MemFree'],data['MemUsage'],data['MemTotal'],data['LoadAvg'], int(data['Time']))
        print "insert OK" 
        ret = c.execute(sql)
    except mysql.IntegrityError:
        pass
    return('OK')
    
if __name__ == '__main__':
    saverD = nbNet('0.0.0.0', 50001, logic)
    saverD.run()


