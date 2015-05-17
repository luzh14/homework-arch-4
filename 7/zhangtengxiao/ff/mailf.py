#!/usr/bin/env python
# coding=utf-8

import smtplib  
from email.mime.text import MIMEText  


def mailf(errdate,biaoti):
    _user = "shishuicer@tom.com"  
    _pwd  = "3edc4rfv"  
    _to   = "zhangtengxiao@ippjr.com"  
      
    msg = MIMEText(errdate)  
    msg["Subject"] = biaoti  
    msg["From"]    = _user  
    msg["To"]      = _to  
      
    s = smtplib.SMTP("smtp.tom.com", timeout=300)  
    s.login(_user, _pwd)  
    s.sendmail(_user, _to, msg.as_string())  
    s.close() 


if __name__=='__main__':
    mailf('neirong','header')
