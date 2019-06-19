import time
import public
from lxml import etree

DB_NAME = 'news'
LIST_API = 'https://m.toutiao.com/list/wxapp/'
DETAIL_API = 'https://m.toutiao.com'
TYPE = [{
        'tag': 'news_society',
        'name': '社会'
        }, {
        'tag': 'news_entertainment',
        'name': '娱乐'
        }, {
        'tag': 'news_tech',
        'name': '科技'
        }, {
        'tag': 'news_car',
        'name': '汽车'
        }, {
        'tag': 'news_military',
        'name': '军事'
        }, {
        'tag': 'news_sports',
        'name': '体育'
        }]
COOKIE = {
    'tt_webid': '6697984343098590727'
}
HEADER = {
    'X-Traffic-Type': 'wxapp',
    'user-agent': 'Mozilla/5.0 (Linux; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00;)AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/18.0.1025 Mobile Safari/537.36 hap/1040/huawei com.huawei.fastapp/1.1.2.300 com.ss.android.article.quickapp/2.0.0 ({"extra":{"original":{"packageName":"com.huawei.appmarket","type":"url"},"scene":"dialog"},"packageName":"com.huawei.android.launcher","type":"shortcut"})'
}


def scrapy_detail(source_url):
    try:
        res = public.request_data(
            DETAIL_API + source_url + 'info/', cookie=COOKIE, header=HEADER).get('data').get('content')

        data = etree.HTML(res)
        detail = []
        for item in data.xpath('//*/div[1]/*'):
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


def scrapy_list(type_info):
    ascp = public.get_ASCP()
    form = {
        'ac': 'wap',
        'format': 'json_raw',
        'min_behot_time': int(time.time()),
        'as': ascp[0],
        'enable_stick': 'false',
        'tag': type_info.get('tag'),
        'cp': ascp[1],
    }
    for item in public.request_data(LIST_API, cookie=COOKIE, header=HEADER, params=form).get('data', []):
        save_data = {
            '_id': public.format_id(item.get('title')),
            'title': item.get('title'),
            'imageurls': list(map(lambda x: x.get('url'), item.get('image_list')))[:3],
            'tag': type_info.get('name'),
            'timestamp': int(time.time()),
            'from': '今日头条',
            'detail': scrapy_detail(item.get('source_url'))
        }
        if save_data.get('detail'):
            public.save_data(save_data, DB_NAME)


def init():
    for i in range(20):
        for type_info in TYPE:
            scrapy_list(type_info)


if __name__ == "__main__":
    init()
