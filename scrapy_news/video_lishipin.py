import time
import public
API = 'https://liteapp.pearvideo.com/web/liteapp/get24hHotConts.jsp'
DB_NAME = 'video'


def init():
    global API
    for i in range(20):
        res = public.request_data(API)
        for item in res.get('contList', []):
            video = {}
            video['_id'] = public.format_id(item.get('name'))
            video['title'] = item.get('name')
            video['from'] = '梨视频'
            video['pic'] = item.get('pic')
            video['url'] = item.get('videos')[0].get('url')
            video['timestamp'] = int(time.time())
            API = res.get('nextUrl')
            public.save_data(video, DB_NAME)


if __name__ == "__main__":
    init()
