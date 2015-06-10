#!/usr/bin/env python
# coding=utf-8

import sys, os
import json
import conf
import mail

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet

host = os.popen('/bin/hostname').read().split()

def MonterMem(d_in):
    data = json.loads(d_in)
    #print data
    alarminfo = conf.ff_conf[0]
    aMU = int(conf.ff_conf[0][2])
    nowMU = int(data['MemUsage'])
    if nowMU > aMU:
        subject_header = 'Subject: %s alarm memusage %s!' % (host, nowMU)
        content = 'please check %s ' % alarminfo
        mail.MailAlarm(subject_header,content)

def MonterLA(d_in):
    data = json.loads(d_in)
    alarminfo = conf.ff_conf[1]
    aLA = int(conf.ff_conf[1][2])
    nowLA = data['LoadAvg']
    if nowLA > aLA:
        subject_header = 'Subject: %s alarm loadavg %s!' % (host, nowMU)
        content = 'please check %s ' % alarminfo
        mail.MailAlarm(subject_header,content)


if __name__ == '__main__':
    def logic(d_in):
        MonterMem(d_in)
        MonterLA(d_in)
        return("OK")
    ffD = nbNet('0.0.0.0', 9652, logic)
    ffD.run()
