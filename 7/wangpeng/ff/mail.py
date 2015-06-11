#!/usr/bin/env python
import smtplib,mimetypes
from email.MIMEText import MIMEText

def MailAlarm(to_addr,subject_header,content):
    mail_server = 'mx1.qq.com'
    mail_server_port = 25
    from_addr = 'alarm@123q.com'
    from_header = 'From: %s\r\n' % (from_addr)
    to_header = 'To: %s\r\n\r\n' % (to_addr)
    m = MIMEText(content)
    m["To"] = to_addr
    m["From"] = from_addr
    m["Subject"] = subject_header

    s = smtplib.SMTP(mail_server, mail_server_port)
    s.sendmail(from_addr, to_addr, m.as_string())
    s.quit()

if __name__ == '__main__':
        MailAlarm(to_addr, subject_header, content)
