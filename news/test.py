import smtplib
from email.mime.text import MIMEText
msg_from = 'ricky@herpstech.com'
passwd = 'hhy19980615,'
msg_to = "1107786871@qq.com"
mail_host = "smtp.mxhichina.com"
port = 465
subject = "python邮件测试"
content = "Hello World"
msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
# 创建连接对象并连接到服务器
s = smtplib.SMTP_SSL(mail_host, port)
# 登录服务器
mail_list = ["1107786871@qq.com"]
s.login(msg_from, passwd)
i = 0
for i in range(0, len(mail_list)):
    msg_to = mail_list[i]
    msg['To'] = msg_to
    s.sendmail(msg_from, msg_to, msg.as_string())
    print("发送成功")
    i = i + 1
