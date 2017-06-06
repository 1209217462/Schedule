#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
mailto_list=['1209217462@qq.com']           #收件人(列表)
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址
mail_user="z1209217462"                           #用户名
mail_pass="163ssqm"                             #密码
mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com

class MyMail():
    def send_mail(to_list, content):
        me = "Schedule" + "<" + mail_user + "@" + mail_postfix + ">"
        msg = MIMEText(content, _subtype='plain')
        msg['Subject'] = '提醒'
        msg['From'] = me
        msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)  # 连接服务器
            server.login(mail_user, mail_pass)  # 登录操作
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            print('send success')
        except Exception:
            print('send failed')
