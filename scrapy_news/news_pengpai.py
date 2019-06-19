from lxml import etree, html
import time
import public
from w3lib.html import remove_tags
from html.parser import HTMLParser

DB_NAME = 'news'
LIST_API = 'http://app.thepaper.cn/clt/jsp/v3/quickAppChannelContList.jsp?WD-UUID=f2bca731-8736-4a82-bc23-35052b16c1f9&uid=95484&WD-VERSION=6.0.0&WD-CLIENT-TYPE=03&n='
DETAIL_API = 'https://m.thepaper.cn/quickApp_jump.jsp?contid='
TYPE = [{
    'name': '时事',
        'tag': '25950',
        },
        {
        'name': '财经',
        'tag': '25951',
        },
        {
        'name': '思想',
        'tag': '25952',
        },
        {
        'name': '生活',
        'tag': '25953',
        }]


def scrapy_detail(contId):
    detail = []
    data = etree.HTML(public.request_html(DETAIL_API + contId))
    info = data.xpath("//*[@class='news_part news_part_limit']/div[1]")[0]
    for item in HTMLParser().unescape(html.tostring(info).decode()).split(
            '<div class="contheight"></div>'):
        content = {}
        if '<img' not in item:
            content['type'] = 'text'
            content['data'] = remove_tags(item)
            detail.append(content)
        else:
            item = etree.HTML(item)
            if item.xpath('//img/@src'):
                content['type'] = 'image'
                content['imgurl'] = item.xpath('//img/@src')[0]
                detail.append(content)
            if item.xpath('//text()'):
                content = {}
                content['type'] = 'text'
                content['data'] = item.xpath('//text()')[0]
                detail.append(content)
    return detail


def scrapy_list(nextUrl, type_info):
    if nextUrl:
        data = public.request_data(nextUrl)
    else:
        data = public.request_data(LIST_API + type_info['tag'])
    for item in data.get('contList', []):
        save_data = {
            '_id': public.format_id(item.get('name')),
            'title': item.get('name'),
            'imageurls': [item.get('pic')],
            'tag': type_info['name'],
            'timestamp': int(time.time()),
            'from': '澎湃新闻',
            'detail': scrapy_detail(item['contId'])
        }
        if save_data.get('detail'):
            public.save_data(save_data, DB_NAME)
    return data.get('nextUrl')


def init():
    for type_info in TYPE:
        next_url = scrapy_list(None, type_info)
        for i in range(20):
            next_url = scrapy_list(
                next_url + '&uuid=f2bca731-8736-4a82-bc23-35052b16c1f9', type_info)


if __name__ == "__main__":
    init()
