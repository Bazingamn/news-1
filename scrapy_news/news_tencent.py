import time
import json
import public

DB_NAME = 'news'
LIST_API = 'http://op.inews.qq.com/coopkyy/mchannel'
DETAIL_API = 'http://op.inews.qq.com/coopkyy/article'
TYPE = [
    {
        'tag': "ent",
        'name': '娱乐'
    }, {
        'tag': "sports",
        'name': '体育'
    }, {
        'tag': "finance",
        'name': '财经'
    }, {
        'tag': "astro",
        'name': '星座'
    }, {
        'tag': "tech",
        'name': '科技'
    }, {
        'tag': "sports_nba",
        'name': 'NBA'
    }, {
        'tag': "milite",
        'name': '军事'
    }, {
        'tag': "digi",
        'name': '数码'
    }, {
        'tag': "fashion",
        'name': '时尚'
    }, {
        'tag': "auto",
        'name': '汽车'
    }, {
        'tag': "games",
        'name': '游戏'
    }, {
        'tag': "house",
        'name': '房产'
    }, {
        'tag': "finance_stock",
        'name': '股票'
    }, {
        'tag': "music",
        'name': '音乐'
    }, {
        'tag': "edu",
        'name': '教育'
    }, {
        'tag': "cul",
        'name': '文化'
    }, {
        'tag': "comic",
        'name': '动漫'
    }, {
        'tag': "world",
        'name': '国际'
    }, {
        'tag': "movie",
        'name': '电影'
    }, {
        'tag': "history",
        'name': '历史'
    }]

HEADER = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00;)AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/18.0.1025 Mobile Safari/537.36 hap/1040/huawei com.huawei.fastapp/1.1.2.300 com.tencent.news.hybrid/2.0.10 ({"extra":{"original":{"packageName":"com.huawei.appmarket","type":"url"},"scene":"dialog"},"packageName":"com.huawei.android.launcher","type":"shortcut"})'
}


def scrapy_detail(id):
    try:
        data = json.loads(public.request_data(
            DETAIL_API + '?id=' + id, header=HEADER).get('data').get('content', []))
        detail = []
        for item in data:
            content = {}
            if item.get('type') == 'cnt_article':
                content['type'] = 'text'
                content['data'] = item.get('desc')
            elif item.get('type') == 'img_url':
                content['type'] = 'image'
                if item.get('img'):
                    content['data'] = item.get('img').get(
                        'imgurl1000').get('imgurl')
                    if not content['data']:
                        content['data'] = item.get('img').get(
                            'imgurl640').get('imgurl')
                    if not content['data']:
                        content['data'] = item.get('img').get(
                            'imgurl0').get('imgurl')
                elif item.get('img_url'):
                    content['data'] = item.get('img_url')
            detail.append(content)
        return detail
    except Exception as e:
        print(e, id)


def scrapy_list(type_info, count):
    form = {
        'channel': type_info.get('tag'),
        'page': count
    }
    data = public.request_data(
        LIST_API, params=form, header=HEADER).get('data', [])
    if data:
        for item in data:
            save_data = {
                '_id': public.format_id(item.get('title')),
                'title': item.get('title'),
                'imageurls': item.get('img_urls'),
                'tag': type_info.get('name'),
                'timestamp': int(time.time()),
                'from': '腾讯新闻',
                'detail': scrapy_detail(item.get('id'))
            }
            if save_data.get('detail'):
                public.save_data(save_data, DB_NAME)


def init():
    for i in range(1, 21):
        for type_info in TYPE:
            scrapy_list(type_info, i)


if __name__ == "__main__":
    init()
