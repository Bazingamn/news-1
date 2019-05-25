# 序列化查询结果
def jsonParse(data):
    res = []
    for item in data:
        if item not in res:
            res.append(item)
    return res
