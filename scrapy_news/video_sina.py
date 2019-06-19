import time
import public
LIST_API = 'http://cre.dp.sina.cn/api/v3/get'
DETAIL_API = 'https://mapi.sina.cn/api/open/quickapp/article/articleinfo'
DB_NAME = 'video'


def init():
    for i in range(20):
        form = {
            'cateid': 'uM',
            'mod': 'mpvideo',
            'action': 1,
            'up': i,
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
            video = {}
            video['_id'] = public.format_id(item.get('title'))
            video['title'] = item.get('title')
            video['from'] = '新浪视频'
            video['pic'] = item.get('thumb')
            video['url'] = public.request_data(
                DETAIL_API, params={'docUrl': item.get('surl')}).get('data').get('videosModule')[0].get('data')[0].get('videoInfo').get('url')
            video['timestamp'] = int(time.time())
            public.save_data(video, DB_NAME)


if __name__ == "__main__":
    init()
