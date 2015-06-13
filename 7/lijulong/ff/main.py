#!/usr/bin/env python
# coding=utf-8
import sys, os
import MySQLdb as mysql
import json
import hashlib
import conf

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from simpleNet.nbNetFramework import nbNet


# mail setting
sender = "lijulongone@163.com"
recivers = "lijulongone@163.com"

show_msg = '来自 {host} 主机的 {api} 超出预设值,请及时作出反馈!!!<br/>'
add_msg = ''

email_theme = '{host} {api} 异常'

class SendMail(object):
    def __init__(self,server='smtp.163.com',account='lijulongone@163.com',passwd='QWERTREWRTREDFCVBGH'):
        self.server = server
        self.account = account
        self.passwd = passwd
        self.server = server
        self.s = smtplib.SMTP(server,25)
        self.s.login(account, passwd)

    def send(self,subject,source,target,msg):
        msg = MIMEText(msg,'html')
        msg['Subject'] = subject
        msg['From'] = source
        msg['To'] = target

        self.s.sendmail(source,target.split(','),msg.as_string())
        logger.info('alert message send successful')
        self.s.quit()

def handleData(value,standart,mark):
    if mark == '=':
        if float(value) == float(standart):
            return True
        else:
            return False
    if mark == '!=':
        if float(value) != float(standart):
            return True
        else:
            return False
    if mark == '>':
        if float(value) > float(standart):
            return True
        else:
            return False
    if mark == '<':
        if float(value)<float(standart):
            return True
        else:
            return False
    if mark == '>=':
        if float(value) > float(standart):
            return True
        else:
            return False
    if mark == '<=':
        if float(value) > float(standart):
            return True
        else:
            return False
    return False
def getResult(d_in):
    try:
        data = json.loads(d_in)
        print data
    except ValueError:
        return []
    # for m in conf.ff_conf:
    #     items.append(m[0])
    datalist=list(data.keys())
    for m in conf.ff_conf:
        if m[0] in datalist:
            if handleData(data[m[0]],m[2],m[1]):
                for user in m[3:]:
                    recivers=recivers+","+user
                sm = SendMail()
                sm.send(email_theme.format(url_name=data['host']),sender,
                    recivers,show_msg.format(host=data['host'],api=m[0])
                    )
    return "OK"

if __name__ == '__main__':
    # if 'MemUsage' in conf.ff_conf[0]:
    #     print "OK"

    def logic(d_in):
        getResult(d_in)
    #print d_in
    #return("OK")

    saverD = nbNet('0.0.0.0', 50252, logic)
    saverD.run()

	