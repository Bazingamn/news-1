from public_api import api as public_api
from news import settings
import pymysql
import os
import sys
import time
import random
import datetime
import json
import requests
sys.path.append('..')
db = pymysql.connect(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['USER'],
                     settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['NAME'], charset='utf8mb4')
cursor = db.cursor()

user_list = [{
    'user_email': '947922112@qq.com',
    'user_passwd': public_api.md5_encode('123'),
    'user_name': '曹芸杨',
    'user_avatar': 'https://uuclock-1254170634.cos.ap-chengdu.myqcloud.com/JSG/user/logo/logo.png',
    'user_gender': 0,
    'user_birth': '1998-06-15',
    'user_location': '成都市'
}, {
    'user_email': '1807915914@qq.com',
    'user_passwd': public_api.md5_encode('123'),
    'user_name': '罗东升',
    'user_avatar': 'https://uuclock-1254170634.cos.ap-chengdu.myqcloud.com/JSG/user/logo/logo.png',
    'user_gender': 0,
    'user_birth': '1998-06-15',
    'user_location': '成都市'
}, {
    'user_email': '944981730@qq.com',
    'user_passwd': public_api.md5_encode('123'),
    'user_name': '何鹏洲',
    'user_avatar': 'https://uuclock-1254170634.cos.ap-chengdu.myqcloud.com/JSG/user/logo/logo.png',
    'user_gender': 0,
    'user_birth': '1998-06-15',
    'user_location': '成都市'
}, {
    'user_email': '1107786871@qq.com',
    'user_passwd': public_api.md5_encode('123'),
    'user_name': '侯海洋',
    'user_avatar': 'https://uuclock-1254170634.cos.ap-chengdu.myqcloud.com/JSG/user/logo/logo.png',
    'user_gender': 0,
    'user_birth': '1998-06-15',
    'user_location': '成都市'
}, {
    'user_email': '1732072083@qq.com',
    'user_passwd': public_api.md5_encode('123'),
    'user_name': '柴英杰',
    'user_avatar': 'https://uuclock-1254170634.cos.ap-chengdu.myqcloud.com/JSG/user/logo/logo.png',
    'user_gender': 0,
    'user_birth': '1998-06-15',
    'user_location': '成都市'
}]

start_index = (2019, 5, 20, 0, 0, 0, 0, 0, 0)
end_index = (2019, 6, 20, 23, 59, 59, 0, 0, 0)
start = time.mktime(start_index)
end = time.mktime(end_index)


def init_user():
    for user in user_list:
        print('当前插入：', user['user_name'])
        INSERT_SQL = '''
                INSERT INTO T_USER(USER_EMAIL,USER_PASSWD,USER_NAME,USER_AVATAR_URL,USER_GENDER,USER_BIRTH,USER_LOCATION)
                VALUES('%s','%s','%s','%s','%s','%s','%s');
                ''' % (user['user_email'], user['user_passwd'], user['user_name'], user['user_avatar'], user['user_gender'], user['user_birth'], user['user_location'])
        cursor.execute(INSERT_SQL)
        db.commit()
    print('初始化账号完成')


def init_use_rec():
    for i in range(1000):
        t = random.randint(start, end)
        date_touple = time.localtime(t)
        date = time.strftime("%Y-%m-%d", date_touple)
        print('插入记录', i, date)
        INSERT_SQL = '''
                INSERT INTO T_USE_REC(USER_ID,USE_TIME) VALUES('%s','%s')
        ''' % (random.randint(1, 5), date)
        cursor.execute(INSERT_SQL)
    db.commit()
    print('初始化使用记录完成')


def init_browse_rec():
    for i in range(10):
        print('初始化：', i)
        news = json.loads(requests.get(
            'http://120.77.144.237/app/getNewsList/').text).get('data')
        for item in news:
            for k in range(random.randint(1, 20)):
                INSERT_SQL = '''
                    INSERT INTO T_BROWSE_REC(USER_ID,NEWS_ID,BROWSE_TIME) VALUES('%s','%s','%s')
                    ''' % (random.randint(1, 5), item['_id'], datetime.date.today())
                cursor.execute(INSERT_SQL)
            db.commit()
    print('初始化浏览记录完成')


if __name__ == "__main__":
    # init_user()
    # init_use_rec()
    # init_browse_rec()
    if os.system('python ../manage.py inspectdb > ../public_api/models.py') == 0:
        print('映射成功')
