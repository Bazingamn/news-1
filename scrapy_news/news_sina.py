import time
import re
import public

DB_NAME = 'news'
LIST_API = 'http://cre.dp.sina.cn/api/v3/get'
DETAIL_API = 'https://mapi.sina.cn/api/open/quickapp/article/articleinfo?docUrl='
TYPE = [
    {
        'category__name': "娱乐",
        'cateid': '1Q',
        'mod': 'mpent'
    }, {
        'category__name': "体育",
        'cateid': '2L',
        'mod': 'mpspt'
    }, {
        'category__name': "财经",
        'cateid': 'y',
        'mod': 'mpfin'
    }, {
        'category__name': "科技",
        'cateid': '1z',
        'mod': 'mptech'},
    {
        'category__name': "军事",
        'cateid': 'F',
        'mod': 'mpmil'
    }]


def scrapy_detail(doc_url):
    try:
        data = public.request_data(
            DETAIL_API + doc_url).get('data')
        if data.get('pics'):
            pics = list(
                map(lambda x: x.get('data').get('pic'), data.get('pics')))
            text = re.split(r'<!--{IMG_\d}-->',
                            data.get('content').replace('<br/>', ''))
            i = 0
            content = []
            for item in text:
                content.append({'type': 'text', 'data': item})
                if i >= 1 and i <= len(text) - 2:
                    content.append({'type': 'image', 'data': pics[i]})
                i += 1
            return content
        elif data.get('picsModule'):
            content = []
            for item in data.get('picsModule')[0].get('data'):
                content.append({'type': 'text', 'data': item.get('alt')})
                content.append({'type': 'image', 'data': item.get('pic')})
            return content
    except Exception as e:
        print(e)


def scrapy_list(type_info, count):
    form = {
        'cateid': type_info['cateid'],
        'mod': type_info['mod'],
        'action': 2,
        'up': count,
        'down': 0,
        'did': '41ea3bde383860b6',
        'imei': '',
        'length': 13,
        'net_type': 2,
        'ad': {"originfrom": "huawei-q", "imei": "868384032192527", "channel": "news_ent", "osVersion": "9", "deviceModel": "HWI-AL00", "platform": "android", "from": "fastapp"},
        'app_type': 124,
        'cre': 'tianyi',
        'merge': 3,
        'statics': 1,
        'ldid': '',
        'uid': ''
    }
    for item in public.request_data(LIST_API, params=form).get('data', []):
        if item.get('thumbs'):
            save_data = {
                '_id': public.format_id(item.get('title')),
                'title': item.get('title'),
                'imageurls': item.get('thumbs')[:3],
                'tag': type_info.get('category__name'),
                'timestamp': int(time.time()),
                'from': '新浪新闻',
                'detail': scrapy_detail(item.get('url'))
            }
            if save_data.get('detail'):
                public.save_data(save_data, DB_NAME)


def init():
    for i in range(20):
        for type_info in TYPE:
            scrapy_list(type_info, i)


if __name__ == "__main__":
    init()
