#coding:utf-8 
from email.mime.text import MIMEText
import smtplib 
import threading


def trysend(to,title,content):
    account=""
    password=""
    server = smtplib.SMTP_SSL('smtp.163.com',465)
    server.docmd("EHLO server" )
    server.login(account,password)
    msg = MIMEText(content)
    msg['Content-Type' ]='text/plain; charset="utf-8"' 
    msg['Subject' ] = title
    msg['From' ] = account
    msg['To' ] = to
    server.sendmail(account, to ,msg.as_string())
    server.close()



def send (to,title,content):
    a=threading.Thread(target=trysend,args=(to,title,content,))
    a.start()
if __name__=="__main__" :
    send("254370469@qq.com" ,"你好,测试一下1111" ,"好好学习,天天向上")
