from django.conf import settings
import pymongo
import json


def jsonParse(data):
    res = []
    for item in data:
        if item not in res:
            res.append(item)
    return res


def get_news_list(request):
    try:
        MYCOL = settings.DB_CON['news']
        return json.dumps({
            'code': 0,
            'data': list(MYCOL.aggregate(
                [{'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timesample': 1, 'from': 1}}, {'$sample': {'size': 10}}]))
        })
    except:
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


def get_video_list(request):
    try:
        MYCOL = settings.DB_CON['video']
        return json.dumps({
            'code': 0,
            'data': list(MYCOL.aggregate(
                [{'$project': {'title': 1, 'url': 1, 'pic': 1, 'timesample': 1, 'from': 1}}, {'$sample': {'size': 10}}]))
        })
    except:
        return json.dumps({
            'code': 1,
            'data': '无法连接到服务器'
        })


if __name__ == "__main__":
    CLIENT = pymongo.MongoClient("mongodb://120.77.144.237:27017")
    DB_CON = CLIENT['news']
    MYCOL = DB_CON['news']
