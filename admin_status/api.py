import json
import uuid
import datetime
import time
import os
import jieba
import requests
from public_api import api as public_api
from public_api import models
from news import settings
import collections
import operator


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
                                public_api.md5_encode(news_passwd) + '\'\n'
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


def get_use_rec(request):
    try:
        start_date = datetime.datetime.strptime(
            request.POST.get('start_date'), '%Y-%m-%d')
        end_date = datetime.datetime.strptime(
            request.POST.get('end_date'), '%Y-%m-%d')
        if (end_date - start_date).days > 0 and (end_date - start_date).days < 32:
            date = get_date(start_date, end_date)
            use_rec = list(map(format_use_rec, public_api.jsonParse(models.TUseRec.objects.filter(
                use_time__gte=start_date, use_time__lte=end_date).values('use_id', 'use_time'))))
            num = [0 for i in range(len(date))]
            for item in use_rec:
                # 如果当前日期不存在访问数据
                if item in date:
                    num[date.index(item)] += 1
            return json.dumps({
                'code': 0,
                'data': {'date': date, 'data': num, 'max': max(num) * 2}
            })
        elif (end_date - start_date).days > 31:
            return json.dumps({
                'code': 1,
                'data': '时间段最多不能超过一个月'
            })
        else:
            return json.dumps({
                'code': 1,
                'data': '起始日期不能大于结束日期'
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })


def format_use_rec_map(item):
    city_name = models.TUser.objects.filter(
        user_id=item.get('user_id')).values('user_location')[0].get('user_location')
    return (item.get('user_id'), city_name)


def get_use_loc(request):
    try:
        today = datetime.date.today()
        user_city = list(map(format_use_rec_map, public_api.jsonParse(models.TUseRec.objects.filter(
            use_time__gte=today, use_time__lte=(today + datetime.timedelta(days=1))).values('use_id', 'user_id'))))
        city_name = set(map(lambda x: x[1], user_city))
        geo_map = {}
        for item in city_name:
            res = requests.get(settings.MAP_API + item).text[27:-1]
            lng_lat = json.loads(res).get('result').get('location')
            geo_map[item] = [lng_lat.get('lng'), lng_lat.get('lat')]
        name_value = dict(collections.Counter(
            list(map(lambda x: x[1], user_city))))
        count_data = []
        for key, value in name_value.items():
            count_data.append({'name': key, 'value': value})
        return json.dumps({
            'code': 0,
            'data': {'geo_map': geo_map, 'count_data': count_data, 'max': max(list(name_value.values()))*2}
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })


def get_date(start_date, end_date):
    date = []
    start_end = (end_date - start_date).days + 1
    for i in range(start_end):
        date.append(
            (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
    return date


def format_use_rec(item):
    return item['use_time'].strftime("%Y-%m-%d")


def get_regist_rec(request):
    try:
        today = datetime.datetime.today()
        end_date = datetime.datetime(
            today.year, today.month, today.day, 0, 0, 0) - datetime.timedelta(days=1)
        start_date = end_date - datetime.timedelta(days=6)
        date = get_date(start_date, end_date)
        regist_rec = list(map(fotmat_regist_rec, public_api.jsonParse(models.TUser.objects.filter(
            sign_up_time__gte=start_date, sign_up_time__lte=end_date).values('user_id', 'sign_up_time'))))
        num = [0 for i in range(7)]
        for item in regist_rec:
            # 如果当前日期不存在访问数据
            if item in date:
                num[date.index(item)] += 1
        return json.dumps({
            'code': 0,
            'data': {'date': date, 'data': num, 'max': max(num) * 2}
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })


def fotmat_regist_rec(item):
    return item['sign_up_time'].strftime("%Y-%m-%d")


def get_hot_news(request):
    try:
        mycol = settings.DB_CON['news']
        today = datetime.date.today()
        data = models.TBrowseRec.objects.filter(
            browse_time__gte=today, browse_time__lte=(today + datetime.timedelta(days=1)))
        data = list(map(lambda x: x['news_id'], data.values('news_id')))
        data = dict(collections.Counter(data))
        data = sorted(data.items(), key=operator.itemgetter(1),
                      reverse=True)[:10]
        res = list(map(format_hot_news, data))
        return json.dumps({
            'code': 0,
            'data': res
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })


def format_hot_news(item):
    mycol = settings.DB_CON['news']
    data = public_api.jsonParse(mycol.find({'_id': item[0]}, {
        'title': 1, 'from': 1, 'tag': 1, 'timestamp': 1}))[0]
    data['title'] = '<a href="/news/' + \
        str(item[0]) + '" target="tab">' + data['title'] + '</a>'
    data['read_num'] = item[1]
    data['time'] = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(data.get('timestamp')))
    return data


def get_hot_search(request):
    try:
        mycol = settings.DB_CON['news']
        today = datetime.date.today()
        data = models.TSearchRec.objects.filter(
            search_time__gte=today, search_time__lte=(today + datetime.timedelta(days=1)))
        # print(data)
        data = list(map(lambda x: x['keyword'],
                        data.values('search_id', 'keyword')))
        # print(data)
        res = []
        words = []
        for item in data:
            words.extend(list(jieba.lcut(item)))
        count_data = dict(collections.Counter(words))
        for key, value in count_data.items():
            res.append({'search_num': value,
                        'keyword': key})
        return json.dumps({
            'code': 0,
            'data': res
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })


def get_today_data(request):
    try:
        mycol = settings.DB_CON['news']
        today = int(time.time()) - int(time.time() - time.timezone) % 86400
        data = {}
        data['news_num'] = list(mycol.aggregate(
            [{'$match': {"timestamp": {"$gte": today}}}, {'$group': {'_id': '', 'news_num': {'$sum': 1}}}]))[0].get('news_num', 0)
        mycol = settings.DB_CON['video']
        data['video_num'] = list(mycol.aggregate(
            [{'$match': {"timestamp": {"$gte": today}}}, {'$group': {'_id': '', 'news_num': {'$sum': 1}}}]))[0].get('news_num', 0)
        data['user_num'] = models.TUseRec.objects.filter(
            use_time__gte=datetime.date.today(), use_time__lte=datetime.date.today()).count()
        return json.dumps({
            'code': 0,
            'data': data
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })


def get_all_data(request):
    try:
        mycol = settings.DB_CON['news']
        data = {}
        data['news_num'] = list(mycol.aggregate(
            [{'$group': {'_id': '', 'news_num': {'$sum': 1}}}]))[0].get('news_num', 0)
        mycol = settings.DB_CON['video']
        data['video_num'] = list(mycol.aggregate(
            [{'$group': {'_id': '', 'news_num': {'$sum': 1}}}]))[0].get('news_num', 0)
        data['registed_user_num'] = models.TUser.objects.all().count()
        data['user_num'] = models.TUseRec.objects.all().count()
        return json.dumps({
            'code': 0,
            'data': data
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '连接服务器失败'
        })
