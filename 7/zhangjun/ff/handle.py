#!/usr/bin/env  python
# -*- coding: UTF-8 -*-


import smtplib  
import sys
from email.mime.text import MIMEText  
from conf import *

def send_mail(username,sub,content):  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = 'tv-v-no@zabbix.com'
    msg['To'] = username
    try:  
        server = smtplib.SMTP()  
        server.connect('localhost')  
        server.sendmail('tv-v-no@zabbix.com', username, msg.as_string())  
        server.close()  
    except Exception, e:  
        print str(e)  
        return False 

def main(data):
    for x in ff_conf:
        if data[x[0]] > x[2]:
            sub = "%s waring" %x[0]
            content = "The %s is used more than %s" %(x[0],x[2])
            send_mail(x[3],sub,content)
