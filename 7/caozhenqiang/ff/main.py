#!/usr/bin/python
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import  nbNet
import json
import sendEmail
def logic(d_in):
    data = json.loads(d_in)
    print data.keys() 
    with open('conf.py') as f:
        content = f.read()
        info_l = eval(content.split('=')[1])
        # [['MemUsage', '>', 1900, 'alarm@qq.com'], ['LoadAvg', '>', 1.0, 'pc@qq.com']]
    for info in info_l:
        key,op,va,mail = info
        expression = str(data[key])+op+str(va)
        print expression
        mail_to = [mail]
        if eval(str(data[key])+op+str(va)): 
            sub_mail = 'Monitor Alarm'
            con_mail = '%s %s %s' %(key,op,va)
            sendEmail.send_mail(mail_to, sub_mail, con_mail)
    return "FF got the data"
transD = nbNet('0.0.0.0', 50002, logic)
transD.run()

