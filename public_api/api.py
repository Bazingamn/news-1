from news import settings
import hashlib
import smtplib


def jsonParse(data):
    res = []
    for item in data:
        if item not in res:
            res.append(item)
    return res


def md5_encode(string):
    salt = settings.SECRET_KEY
    string = string + salt
    md = hashlib.md5()
    md.update(string.encode())
    return md.hexdigest()


def send_email(to_email, msg):
    try:
        # settings.SMTP.ehlo()
        SMTP = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        SMTP.connect(settings.EMAIL_HOST)
        SMTP.login(settings.EMAIL_HOST_USER,
                   settings.EMAIL_HOST_PASSWORD)
        SMTP.sendmail(settings.DEFAULT_FROM_EMAIL,
                      to_email, msg.as_string())
        return True
    except Exception as e:
        print(e)
