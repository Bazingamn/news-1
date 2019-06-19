import time
import re
import public
from lxml import etree

DB_NAME = 'news'
LIST_API = 'http://api.iclient.ifeng.com/ClientNews'
DETAIL_API = 'https://api.3g.ifeng.com/ipadtestdoc'
TYPE = [
    {
        'tag': "YL53,FOCUSYL53",
        'name': '娱乐'
    }, {
        'tag': "CJ33,FOCUSCJ33,HNCJ33",
        'name': '财经'
    }, {
        'tag': "TY43,FOCUSTY43,TYLIVE",
        'name': '体育'
    }, {
        'tag': "KJ123,FOCUSKJ123",
        'name': '科技'
    }, {
        'tag': "JS83,FOCUSJS83",
        'name': '军事'
    }]


def scrapy_detail(aid):
    try:
        form = {
            'st': '',
            'df': 'androidphone',
            'loginid': '',
            'os': 'android',
            'city': '',
            'screen': '1080x1794',
            'nw': 'wifi',
            'deviceid': '',
            'publishid': '5286',
            'gv': '5.7.2',
            'uid': '868384032192527',
            'province': '',
            'av': '5.7.2',
            'proid': 'ifengnews',
            'district': '',
            'limit': 5,
            'from': 'xiaomi',
            'sn': '',
            'aid': aid,
            'vt': 5,
        }
        res = public.request_data(
            DETAIL_API, params=form).get('body').get('text')
        data = etree.HTML(res)
        detail = []
        for item in data.xpath('//*'):
            if item.xpath('text()'):
                content = {}
                content['type'] = 'text'
                content['data'] = item.xpath('text()')[0]
                detail.append(content)
            if item.xpath('img/@src'):
                content = {}
                content['type'] = 'image'
                content['data'] = item.xpath('img/@src')[0]
                detail.append(content)
        return detail
    except Exception as e:
        print(e)


def scrapy_list(type_info, count):
    form = {
        'st': '',
        'df': '',
        'pullNum': count,
        'loginid': '',
        'os': 'android',
        'city': '',
        'screen': '',
        'nw': '',
        'deviceid': '',
        'gv': '5.7.3',
        'publishid': '',
        'uid': '868384032192527',
        'lastDoc': '',
        'province': '',
        'av': 0,
        'district': '',
        'proid': 'ifengnews',
        'action': 'default',
        'id': type_info.get('tag'),
        'sn': '',
        'vt': 5,
    }
    data = public.request_data(LIST_API, params=form)[0]
    if data:
        for item in data.get('item'):
            if item.get('thumbnail') and item.get('id'):
                save_data = {
                    '_id': public.format_id(item.get('title')),
                    'title': item.get('title'),
                    'imageurls': [item.get('thumbnail')],
                    'tag': type_info.get('name'),
                    'timestamp': int(time.time()),
                    'from': '凤凰新闻',
                    'detail': scrapy_detail(item.get('id'))
                }
                if save_data.get('detail'):
                    public.save_data(save_data, DB_NAME)


def init():
    for i in range(20):
        for type_info in TYPE:
            scrapy_list(type_info, i)


if __name__ == "__main__":
    init()
