import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

class SendEmail:
    global send_user
    global email_host
    global password
    email_host = "smtp.qq.com"
    send_user = "380222985@qq.com"
    password = "eyteexarlvghbhhg"



    def send_main(self,count):
        # 邮件发送给谁
        #'lishuailei_v@zuoyebang.com'
        user_list = ['380222985@qq.com']

        user = "测试报告" + "<" + send_user + ">"
        message = MIMEMultipart()

        message['From'] = user
        message['To'] = ";".join(user_list)
        content = "app  carch数量为为{}".format(count)
        sub = content
        message['Subject'] = sub

        filename = 'log/anr_traces.log'
        time = datetime.date.today()
        att = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s_anr_traces.txt"' % time
        message.attach(att)

        apifilename = 'log/logcat.Log'
        time = datetime.date.today()
        att = MIMEText(open(apifilename, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s_logcat.txt"' % time
        message.attach(att)

        #windows发送邮件
        server = smtplib.SMTP()
        server.connect(email_host)
        #linux发送邮件
        # server=smtplib.SMTP_SSL(email_host,465)
        server.login(send_user, password)
        server.sendmail(send_user,user_list,message.as_string())
        server.close()

if __name__ == '__main__':
    sen = SendEmail()
    sen.send_main(2)