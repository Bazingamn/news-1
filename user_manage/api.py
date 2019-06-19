from django.conf import settings
from django.core.mail import send_mail
from news import settings
import json
import random
import time
import requests
from public_api import models, fileIO, cosFile
from public_api import api as public_api
from email.mime.text import MIMEText


def getCode():
    code = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch
    return code


def send_check_code(request):
    try:
        user_email = request.POST.get('user_email')
        check_code = getCode()
        msg = MIMEText('您的验证码为%s,15分钟内有效，【新闻APP】' % (check_code))
        msg['Subject'] = '新闻APP'
        msg['From'] = '新闻APP'
        msg['To'] = user_email
        if user_email:
            if public_api.send_email(user_email, msg):
                request.session['check_code'] = check_code
                return json.dumps({
                    'code': 0,
                    'data': '发送成功'
                })
            else:
                return json.dumps({
                    'code': 1,
                    'data': '发送失败'
                })
        else:
            return json.dumps({
                'code': 1,
                'data': '请输入邮箱'
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def sign_up(request):
    try:
        user_email = request.POST.get('user_email')
        user_passwd = request.POST.get('user_passwd')
        user_name = request.POST.get('user_name')
        user_avatar_url = settings.DETAULT_AVATAR
        user_gender = request.POST.get('user_gender')
        user_birth = request.POST.get('user_birth')
        user_location = request.POST.get('user_location')
        user_introduce = request.POST.get('user_introduce')
        in_check_code = request.POST.get('check_code')
        if not user_location:
            if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            header = {'Authorization': 'APPCODE ' + settings.LOCATION_APPCODE}
            user_location = json.loads(requests.get(
                settings.LOCATION_API + ip, headers=header).text).get('data').get('city')
        print(user_email, user_passwd, user_name, user_avatar_url, user_gender,
              user_birth, user_location, request.session.get('check_code'))
        print(request.session.get('check_code'))
        if in_check_code == request.session.get('check_code'):
            models.TUser.objects.create(user_email=user_email, user_passwd=user_passwd, user_name=user_name,
                                        user_avatar_url=user_avatar_url, user_gender=user_gender, user_birth=user_birth, user_location=user_location, user_introduce=user_introduce)
            return json.dumps({
                'code': 0,
                'data': '注册成功'
            })
        else:
            return json.dumps({
                'code': 1,
                'data': '注册失败，验证码错误'
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def modify_user_info(request):
    try:
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        user_gender = request.POST.get('user_gender')
        user_birth = request.POST.get('user_birth')
        user_location = request.POST.get('user_location')
        user_introduce = request.POST.get('user_introduce')
        if not user_location:
            if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            header = {'Authorization': 'APPCODE ' + settings.LOCATION_APPCODE}
            user_location = json.loads(requests.get(
                settings.LOCATION_API + ip, headers=header).text).get('data').get('city')
        user = models.TUser.objects.get(user_id=user_id)
        user.user_name = user_name
        user.user_gender = user_gender
        user.user_birth = user_birth
        user.user_location = user_location
        user.user_introduce = user_introduce
        user.save()
        return json.dumps({
            'code': 0,
            'data': '修改成功'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def modify_logo(request):
    filename = str(time.time()) + '.jpg'
    try:
        user_avatar_url = request.FILES.get("user_logo")
        print(user_avatar_url)
        user_id = request.POST.get('user_id')
        if fileIO.setFile(filename, user_avatar_url) == 0:
            user_avatar_url = models.TUser.objects.filter(
                user_id=user_id).values()[0].get('user_avatar_url')
            oldpath = 'newsapp/user/logo/' + user_avatar_url.split('/')[-1]
            cosFile.delete(oldpath)
            path = 'newsapp/user/logo/' + filename
            url = cosFile.up(fileIO.getFile(filename), path)
            models.TUser.objects.filter(
                user_id=user_id).update(user_avatar_url=url)
            return json.dumps({
                'code': 0,
                'data': {'msg': '修改成功', 'url': url}
            })
        else:
            return json.dumps({
                'code': 1,
                'data': '上传头像失败'
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def login(request):
    try:
        user_email = request.POST.get('user_email', '')
        user_passwd = request.POST.get('user_passwd', '')
        print(user_email, user_passwd)
        user_info = models.TUser.objects.filter(
            user_email=user_email, user_passwd=user_passwd)
        if user_info.count() == 1:
            user_info = list(map(format_user_info, public_api.jsonParse(user_info.values(
                'user_id', 'user_email', 'user_name', 'user_gender', 'user_avatar_url', 'user_birth', 'user_location', 'user_introduce'))))
            request.session['user_id'] = user_info[0].get('user_id')
            return json.dumps({
                'code': 0,
                'data': user_info
            })
        else:
            return json.dumps({
                'code': 1,
                'data': '登录失败，用户名或密码错误'
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def format_user_info(item):
    item['user_birth'] = item['user_birth'].strftime("%Y-%m-%d")
    return item
