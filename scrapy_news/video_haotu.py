import time
import public
LIST_API = 'https://howtodos.yladm.com/video/v2/head'
DETAIL_API = 'https://howtodos.yladm.com/video/play?app=qucikapp&id='
CHANNEL_IDS = [100, 153, 104, 101, 115, 106, 108, 109, 102, 103, 112, 117, 107]
DB_NAME = 'video'


def init():
    for channel_id in CHANNEL_IDS:
        for i in range(20):
            form = {
                'app': 'howto_a',
                'udid': '41ea3bde383860b6',
                'channel_id': channel_id,
                'timestamp': int(time.time())
            }
            for item in public.request_data(LIST_API, params=form).get('contents', []):
                video = {}
                video['_id'] = public.format_id(item.get('video').get('name'))
                video['title'] = item.get('video').get('name')
                video['from'] = '好兔视频'
                video['pic'] = item.get('video').get('share_img')
                video['url'] = public.request_data(
                    DETAIL_API, params={'id': item.get('id')}).get('bitrates')[-1].get('uri')
                video['timestamp'] = int(time.time())
                public.save_data(video, DB_NAME)


if __name__ == "__main__":
    init()
