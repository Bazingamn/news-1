import time
import json
import public
from lxml import etree

DB_NAME = 'news'
LIST_API = 'https://3g.163.com/touch/reconstruct/article/list/'
DETAIL_API = 'https://api.3g.ifeng.com/ipadtestdoc'
TYPE = [
    {
        'tag': "DDBVD5B3wangning",
        'name': '头条'
    }, {
        'tag': "BA10TA81wangning",
        'name': '娱乐'
    }, {
        'tag': "BA8E6OEOwangning",
        'name': '体育'
    }, {
        'tag': "BA8DOPCSwangning",
        'name': '汽车'
    }, {
        'tag': "BA8D4A3Rwangning",
        'name': '科技'
    }, {
        'tag': "BA8EE5GMwangning",
        'name': '财经'
    }, {
        'tag': "BAI5E21Owangning",
        'name': '独家'
    }]


def scrapy_detail(url):
    try:
        data = etree.HTML(public.request_html(url))
        detail = []
        for item in data.xpath("//*[@class='page js-page on']/*"):
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
            if item.xpath('a/img/@src'):
                content = {}
                content['type'] = 'image'
                content['data'] = item.xpath('a/img/@src')[0]
                detail.append(content)
        return detail
    except Exception as e:
        print(e, url)


def scrapy_list(type_info, count):
    url = '%s%s/%s-%s.html' % (LIST_API, type_info.get('tag'),
                               str(count * 10), str((count + 1) * 10))
    for item in json.loads(public.request_html(url)[9:-1]).get(type_info.get('tag', [])):
        if item.get('url').startswith('http'):
            save_data = {
                '_id': public.format_id(item.get('title')),
                'title': item.get('title'),
                'imageurls': [item.get('imgsrc')],
                'tag': type_info.get('name'),
                'timestamp': int(time.time()),
                'from': '网易新闻',
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
