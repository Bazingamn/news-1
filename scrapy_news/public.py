import requests
import pymongo
import logging
from fake_useragent import UserAgent
import json
import hashlib
import time
import random
import math
from urllib import parse
import binascii
from requests.packages import urllib3
urllib3.disable_warnings()
USER_AGENT = UserAgent()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
client = pymongo.MongoClient("mongodb://***:27017")
db = client['news']


# 请求数据
def request_data(url, params=None, cookie=None, header=None, method='GET', debug=False):
    try:
        if not header:
            header = {"User-Agent": USER_AGENT.random}
        if method == 'GET':
            res = requests.get(url, params=params,
                               cookies=cookie, headers=header, verify=False)
        else:
            res = requests.post(url, params=params,
                                cookies=cookie, headers=header, verify=False)
        if debug:
            print(res.text)
        data = json.loads(res.text)
        if not data or res.status_code != 200:
            return {}
        else:
            return data
    except Exception as e:
        logging.warning(url)
        logger.warning(e)
        return {}


# 请求html
def request_html(url, params=None, cookie=None, header=None):
    try:
        if not header:
            header = {"User-Agent": USER_AGENT.random}
        res = requests.get(url, params=params,
                           cookies=cookie, headers=header, verify=False)
        return res.text
    except Exception as e:
        logging.warning(url)
        logger.warning(e)
        return {}


# 保存数据
def save_data(data, db_name):
    try:
        mycol = db[db_name]
        mycol.insert_one(data)
        logger.info('save success\t' + data.get('title'))
    except Exception as e:
        # logger.warning(e)
        pass


# 格式化id
def format_id(title):
    try:
        md = hashlib.md5()
        md.update(title.encode())
        return int(''.join(list(filter(str.isdigit, md.hexdigest())))[:9])
    except Exception as e:
        logger.warning(e)


# 今日头条ASCP获取
def get_ASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS, CP

    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS, CP


# 今日头条RS获取
def get_rs(video_id):
    r = str(random.random())[2:]
    url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/{}'.format(video_id)
    n = parse.urlparse(url).path + '?r=' + r
    c = binascii.crc32(n.encode())
    s = c >> 0 if c >= 0 else (c + 0x100000000) >> 0
    return r, s
