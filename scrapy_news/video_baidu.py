import time
import public
CHANNELS = ['recnewslist', 'amuse', 'yuanchuang', 'yule',
            'info', 'squaredance', 'education', 'horrible', 'predefine8']
LIST_API = 'http://m.v.baidu.com/fastapp/short'
DETAIL_API = 'http://m.v.baidu.com/fastapp/watch'
DB_NAME = 'video'


def init():
    for channel in CHANNELS:
        for i in range(20):
            for item in public.request_data(LIST_API, params={'channel': channel, 'page': i}).get('videos', []):
                video = {}
                video['_id'] = public.format_id(item.get('title'))
                video['title'] = item.get('title')
                video['from'] = '百度视频'
                video['pic'] = item.get('imgh_url')
                video['url'] = public.request_data(
                    DETAIL_API, params={'id': item.get('url').split('/')[-1].split('.')[0]}).get('data').get('main_video').get('source').get('mp4')
                video['timestamp'] = int(time.time())
                public.save_data(video, DB_NAME)


if __name__ == "__main__":
    init()
