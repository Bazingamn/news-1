from news import settings
import hashlib

# 序列化查询结果


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
