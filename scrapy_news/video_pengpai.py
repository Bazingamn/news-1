import time
import public
from lxml import etree
LIST_API = 'https://app.thepaper.cn/clt/jsp/v3/quickAppChannelContList.jsp?WD-UUID=ac2f8b6c-be2f-4f2e-85ff-7f8625f4589c&uid=95484&WD-VERSION=6.0.0&WD-CLIENT-TYPE=03&n=-4'
DETAIL_API = 'https://m.thepaper.cn/quickApp_jump.jsp'
DB_NAME = 'video'
FORM = {
    'uuid': 'ac2f8b6c-be2f-4f2e-85ff-7f8625f4589c?uuid=ac2f8b6c-be2f-4f2e-85ff-7f8625f4589c'
}


def init():
    global LIST_API
    for i in range(20):
        res = public.request_data(LIST_API, params=FORM)
        for item in res.get('contList', []):
            video = {}
            video['_id'] = public.format_id(item.get('name'))
            video['title'] = item.get('name')
            video['from'] = '澎湃视频'
            video['pic'] = item.get('pic')
            video['url'] = etree.HTML(public.request_html(
                DETAIL_API, params={'contid': item['contId']})).xpath("//*[@class='m']/@href")[0]
            video['timestamp'] = int(time.time())
            LIST_API = res.get('nextUrl')
            public.save_data(video, DB_NAME)


if __name__ == "__main__":
    init()
