import pymongo
import time
from urllib import request
client = pymongo.MongoClient("mongodb://120.77.144.237:27017")
db = client['news']
mycol = db['video']


def check():
    while True:
        i = 1
        for item in mycol.find():
            try:
                with request.urlopen(item.get('url')) as file:
                    if file.status == 200:
                        print(i, file.status, '未失效', item.get('_id'))
                    else:
                        print('已失效', item.get('_id'))
                        mycol.delete_one({'_id': item.get('_id')})
                    i += 1
            except Exception as e:
                print(e)
                print('已失效', item.get('_id'))
                mycol.delete_one({'_id': item.get('_id')})
                i += 1
                continue


if __name__ == "__main__":
    check()
