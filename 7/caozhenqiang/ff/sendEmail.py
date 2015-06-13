#!/usr/bin/env python
#coding=utf8
import smtplib
from email.mime.text import MIMEText

def send_mail(mail_to, subject, content):
    smtp_server = 'smtp.sina.com'
    mail_user = 'reboothomework'
    mail_pass = 'reboot@123'
    mail_postfix = 'sina.com'
    me = mail_user+'@'+mail_postfix 
    msg = MIMEText(content,_subtype='plain',_charset='utf8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ';'.join(mail_to)
    try:
        s = smtplib.SMTP(smtp_server)
        s.set_debuglevel(1)
        s.login(mail_user, mail_pass)
        s.sendmail(me,mail_to,msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    mailto_list = ['xiaoqiang0419@163.com','xiaoqiang0419@sina.cn']
    if send_mail(mailto_list,"hello","hello world!"):
        print 'SUCCESS'
    else:
        print 'UNSUCCESS'





