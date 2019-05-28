import json
import uuid
import os
from public_api import api as public_api
from news import settings


def login(request):
    try:
        user_name = request.POST.get('username')
        passwd = request.POST.get('password')
        tocken = str(uuid.uuid4()).replace('-', '')
        request.session['tocken'] = tocken
        if user_name == 'admin' and public_api.md5_encode(passwd) == settings.PASSWD:
            return json.dumps({
                'code': 0,
                'data': '登录成功'
            })
        else:
            return json.dumps({
                'code': 1,
                'data': '账号或密码错误'
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })


def modify_passwd(request):
    try:
        old_passwd = request.POST.get('old_passwd')
        news_passwd = request.POST.get('news_passwd')
        new_passwd_again = request.POST.get('new_passwd_again')
        if news_passwd == new_passwd_again:
            if public_api.md5_encode(old_passwd) == settings.PASSWD:
                settings.PASSWD = public_api.md5_encode(news_passwd)
                lines = []
                with open(os.path.join(settings.BASE_DIR, 'news', 'settings.py'), 'r') as f:
                    for line in f:
                        lines.append(line)
                with open(os.path.join(settings.BASE_DIR, 'news', 'settings.py'), 'w') as f:
                    for line in lines:
                        if line.startswith('PASSWD'):
                            line = 'PASSWD = \'' + \
                                public_api.md5_encode(news_passwd)+'\'\n'
                        f.writelines(line)
                return json.dumps({
                    'code': 0,
                    'data': '修改成功'
                })
            else:
                return json.dumps({
                    'code': 1,
                    'data': '原密码错误'
                })
        else:
            return json.dumps({
                'code': 1,
                'data': '两次输入的密码不一致'
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })
