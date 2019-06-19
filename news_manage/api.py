from django.conf import settings
import pymongo
import json
import re
import time
from public_api import models
from public_api import api as public_api


def format_time(item):
    item['timestamp'] = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(item['timestamp']))
    return item


def get_news_list(request):
    try:
        news_type = request.GET.get('news_type')
        MYCOL = settings.DB_CON['news']
        if news_type:
            return json.dumps({
                'code': 0,
                'data': list(MYCOL.aggregate(
                    [{'$match': {'tag': news_type}}, {'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timestamp': 1, 'from': 1}}, {'$sample': {'size': 10}}], allowDiskUse=True))
            })
        else:
            return json.dumps({
                'code': 0,
                'data': list(MYCOL.aggregate(
                    [{'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timestamp': 1, 'from': 1}}, {'$sample': {'size': 10}}], allowDiskUse=True))
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def search_news(request):
    try:
        keyword = request.GET.get('keyword')
        user_id = request.GET.get('user_id')
        if user_id != '-1' and user_id:
            models.TSearchRec.objects.create(
                user=models.TUser.objects.get(user_id=user_id), keyword=keyword)
        MYCOL = settings.DB_CON['news']
        if keyword:
            return json.dumps({
                'code': 0,
                'data': list(MYCOL.aggregate(
                    [{'$match': {'title': re.compile(keyword)}}, {'$sort': {'timestamp': -1}}, {'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timestamp': 1, 'from': 1}}, {'$sample': {'size': 10}}]))
            })
        else:
            return json.dumps({
                'code': 0,
                'data': list(MYCOL.aggregate(
                    [{'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timestamp': 1, 'from': 1}}, {'$sort': {'timestamp': -1}}, {'$sample': {'size': 10}}]))
            })
    except:
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def get_video_list(request):
    try:
        MYCOL = settings.DB_CON['video']
        keyword = request.GET.get('keyword')
        if not keyword:
            return json.dumps({
                'code': 0,
                'data': list(map(format_time, MYCOL.aggregate(
                    [{'$project': {'title': 1, 'url': 1, 'pic': 1, 'timestamp': 1, 'from': 1}}, {'$sort': {'timestamp': -1}}, {'$sample': {'size': 10}}])))
            })
        else:
            return json.dumps({
                'code': 0,
                'data': list(map(format_time, MYCOL.aggregate(
                    [{'$match': {'title': re.compile(keyword)}}, {'$project': {'title': 1, 'url': 1, 'pic': 1, 'timestamp': 1, 'from': 1}}, {'$sort': {'timestamp': -1}}, {'$sample': {'size': 10}}])))
            })
    except:
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def get_recommend_list(request):
    try:
        user_id = request.GET.get('user_id')
        page = int(request.GET.get('page'))
        MYCOL = settings.DB_CON['news']
        if user_id != '-1' and user_id:
            obj = models.TRecommend.objects
            obj = obj.order_by(
                "-time")
            obj = obj.order_by(
                "-rating")
            new_ids = list(map(lambda x: x['product'], public_api.jsonParse(obj.filter(
                user=models.TUser.objects.get(user_id=user_id))[page * 10:(page + 1) * 10].values('product'))))
            if not new_ids:
                return json.dumps({
                    'code': 0,
                    'data': list(MYCOL.aggregate(
                        [{'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timestamp': 1, 'from': 1}}, {'$sort': {'timestamp': -1}}, {'$sample': {'size': 10}}]))
                })
            else:
                res = []
                for new_id in new_ids:
                    news = list(MYCOL.aggregate(
                        [{'$match': {'_id': new_id}}, {'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timestamp': 1, 'from': 1}}, {'$sort': {'timestamp': -1}}, {'$sample': {'size': 10}}]))
                    if not news:
                        delete_news(new_id)
                    else:
                        res.extend(news)
                return json.dumps({
                    'code': 0,
                    'data': res
                })
        else:
            return json.dumps({
                'code': 0,
                'data': list(MYCOL.aggregate(
                    [{'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timestamp': 1, 'from': 1}}, {'$sort': {'timestamp': -1}}, {'$sample': {'size': 10}}]))
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def delete_news(news_id):
    models.TBrowseRec.objects.filter(news_id=news_id).delete()
    models.TCollection.objects.filter(news_id=news_id).delete()
    models.TComment.objects.filter(news_id=news_id).delete()


def get_type_list(request):
    try:
        MYCOL = settings.DB_CON['news']
        return json.dumps({
            'code': 0,
            'data': list(MYCOL.find({}, {'$project': {'_id': 0, 'tag': 1}}).distinct('tag'))
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def get_news_detail(request):
    try:
        MYCOL = settings.DB_CON['news']
        news_id = request.GET.get('_id')
        user_id = request.GET.get('user_id')
        if user_id != '-1' and user_id:
            models.TBrowseRec.objects.create(
                user=models.TUser.objects.get(user_id=user_id), news_id=news_id)
        data = list(MYCOL.find({'_id': int(news_id)}))
        if not data:
            delete_news(news_id)
        return json.dumps({
            'code': 0,
            'data': data
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def collect_news(request):
    try:
        news_id = int(request.GET.get('_id'))
        user_id = request.GET.get('user_id')
        data = models.TCollection.objects.filter(
            user=models.TUser.objects.get(user_id=user_id), news_id=news_id)
        if data.count() == 1:
            data.delete()
            return json.dumps({
                'code': 0,
                'data': '取消收藏成功'
            })
        else:
            models.TCollection.objects.create(
                user=models.TUser.objects.get(user_id=user_id), news_id=news_id)
            return json.dumps({
                'code': 0,
                'data': '收藏成功'
            })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def get_collect_news(request):
    try:
        user_id = request.GET.get('user_id')
        page = int(request.GET.get('page', 0))
        obj = models.TCollection.objects
        data = public_api.jsonParse(obj.filter(
            user=models.TUser.objects.get(user_id=user_id))[page * 10:(page + 1) * 10].values())
        print(data)
        return json.dumps({
            'code': 0,
            'data': list(filter(None, list(map(format_collect_rec, data))))
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def format_collect_rec(item):
    MYCOL = settings.DB_CON['news']
    item['news_info'] = list(MYCOL.find({'_id': int(item['news_id'])}))
    item['collect_time'] = item['collect_time'].strftime(
        "%Y-%m-%d %H:%M:%S")
    if len(item['news_info']) == 1:
        del item['news_info'][0]['detail']
        del item['news_id']
        return item
    else:
        delete_news(item['news_id'])


def delete_collect_news(request):
    try:
        news_id = int(request.GET.get('_id'))
        user_id = request.GET.get('user_id')
        models.TCollection.objects.filter(
            user=models.TUser.objects.get(user_id=user_id), news_id=news_id).delete()
        return json.dumps({
            'code': 0,
            'data': '删除成功'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def delete_all_collect(request):
    try:
        user_id = request.GET.get('user_id')
        models.TCollection.objects.filter(
            user=models.TUser.objects.get(user_id=user_id)).delete()
        return json.dumps({
            'code': 0,
            'data': '删除成功'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def check_collect(request):
    try:
        news_id = int(request.GET.get('_id'))
        user_id = request.GET.get('user_id')
        count = models.TCollection.objects.filter(
            user=models.TUser.objects.get(user_id=user_id), news_id=news_id).count()
        return json.dumps({
            'code': 0,
            'data': count
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def get_comment(request):
    try:
        user_id = request.GET.get('user_id')
        page = int(request.GET.get('page', 0))
        obj = models.TComment.objects
        data = public_api.jsonParse(obj.filter(
            user=models.TUser.objects.get(user_id=user_id))[page * 10:(page + 1) * 10].values())
        return json.dumps({
            'code': 0,
            'data': list(filter(None, list(map(format_comment_rec, data))))
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def format_comment_rec(item):
    MYCOL = settings.DB_CON['news']
    item['news_info'] = list(MYCOL.find({'_id': int(item['news_id'])}))
    item['comment_time'] = item['comment_time'].strftime(
        "%Y-%m-%d %H:%M:%S")
    if len(item['news_info']) == 1:
        del item['news_info'][0]['detail']
        del item['news_id']
        return item
    else:
        delete_news(item['news_id'])


def get_news_comment(request):
    try:
        news_id = int(request.GET.get('_id'))
        page = int(request.GET.get('page', 0))
        data = public_api.jsonParse(models.TComment.objects.filter(
            news_id=news_id)[page * 10:(page + 1) * 10].values())
        data = list(map(format_news_comment, data))
        return json.dumps({
            'code': 0,
            'data': data
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def format_news_comment(item):
    data = public_api.jsonParse(
        models.TUser.objects.filter(user_id=item['user_id']).values('user_id', 'user_name', 'user_avatar_url'))[0]
    data['comment_id'] = item['comment_id']
    data['comment_time'] = item['comment_time'].strftime("%Y-%m-%d %H:%M:%S")
    data['comment_text'] = item['comment_text']
    return data


def add_comment(request):
    try:
        news_id = request.GET.get('_id')
        user_id = request.GET.get('user_id')
        comment_text = request.GET.get('comment_text')
        models.TComment.objects.create(news_id=news_id, user=models.TUser.objects.get(
            user_id=user_id), comment_text=comment_text)
        return json.dumps({
            'code': 0,
            'data': '评论成功'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def delete_comment(request):
    try:
        comment_id = request.GET.get('comment_id')
        user_id = request.GET.get('user_id')
        models.TComment.objects.filter(
            user=models.TUser.objects.get(user_id=user_id), comment_id=comment_id).delete()
        return json.dumps({
            'code': 0,
            'data': '删除成功'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def delete_all_comment(request):
    try:
        user_id = request.GET.get('user_id')
        models.TComment.objects.filter(
            user=models.TUser.objects.get(user_id=user_id)).delete()
        return json.dumps({
            'code': 0,
            'data': '删除成功'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


if __name__ == "__main__":
    CLIENT = pymongo.MongoClient("mongodb://120.77.144.237:27017")
    DB_CON = CLIENT['news']
    MYCOL = DB_CON['news']
