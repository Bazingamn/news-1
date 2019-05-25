from django.conf import settings
import pymongo


def jsonParse(data):
    res = []
    for item in data:
        if item not in res:
            res.append(item)
    return res


def get_news_list(request):
    return list(settings.MYCOL.aggregate(
        [{'$project': {'title': 1, 'imageurls': 1, 'tag': 1, 'timesample': 1, 'from': 1}}, {'$sample': {'size': 10}}]))


if __name__ == "__main__":
    CLIENT = pymongo.MongoClient("mongodb://120.77.144.237:27017")
    DB_CON = CLIENT['news']
    MYCOL = DB_CON['news']
