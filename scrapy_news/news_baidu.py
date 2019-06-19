import json
import time
import re
import uuid
import public
DB_NAME = 'news'
LISTAPI = 'https://news.baidu.com/sn/api/feed_feedlist'
DETAILAPI = 'https://news.baidu.com/news?tn=bdapibaiyue&t=recommendinfo'
pattern = re.compile(r'<[^>]+>', re.S)
category__names = ['娱乐', '军事', '科技', '生活', '国际', '国内', '体育', '汽车']


def format_detail(item):
    data = {}
    data['type'] = item.get('type')
    if item.get('type') == 'text':
        data['data'] = pattern.sub('', item.get('data'))
    else:
        data['data'] = item.get('data').get('original').get('url')
    return data


def scrapy_detail(nid, tag):
    try:
        detail_postdata = {
            'cuid': '',
            'nids': nid,
            'wf': 1,
            'remote_device_type': 1,
            'os_type': 1,
            'screen_size_width': 1080,
            'screen_size_height': 1920,
        }
        data = public.request_data(
            DETAILAPI, params=detail_postdata).get('data').get('news')[0]
        return list(map(format_detail, data.get('content')))
    except Exception as e:
        print(e, 1)


def scrapy_list(cookie, category__name, timesample):
    list_postdata = {
        'from': 'news_webapp',
        'pd': 'webapp',
        'os': 'android',
        'mid': cookie['BAIDUID'],
        'ver': 6,
        'category_name': category__name,
        'action': 0,
        'display_time': timesample,
        'wf': 0,
    }
    data = public.request_data(
        LISTAPI, params=list_postdata, cookie=cookie).get('data').get('news', [])
    for item in data:
        save_data = {
            '_id': public.format_id(item.get('title')),
            'title': item.get('title'),
            'imageurls': list(map(lambda x: x.get('url_webp', ''), item.get('imageurls', []))),
            'tag': category__name,
            'timestamp': int(time.time()),
            'from': '百度新闻',
                    'detail': scrapy_detail(item.get('nid'), category__name)
        }
        if save_data.get('detail') and len(save_data.get('detail')) > 1:
            public.save_data(save_data, DB_NAME)


def init():
    cookie = {
        'BIDUPSID': str(uuid.uuid4()).replace('-', ''),
        'BAIDUID': str(uuid.uuid4()).replace('-', '') + ':FG=1',
        'HMACCOUNT': 'E1D5995C5F3B0F74'
    }
    for category__name in category__names:
        timesample = str(int(time.time()))
        for i in range(20):
            timesample = scrapy_list(cookie, category__name, timesample)


if __name__ == "__main__":
    init()
