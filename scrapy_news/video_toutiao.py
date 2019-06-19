import time
import public

import base64

LIST_API = 'https://m.toutiao.com/list/wxapp/'
DETAIL_API = 'https://ib.365yg.com/video/urls/v/1/toutiao/mp4/'
DB_NAME = 'video'
COOKIE = {
    'tt_webid': '6697984343098590727'
}
HEADER = {
    'X-Traffic-Type': 'wxapp',
    'user-agent': 'Mozilla/5.0 (Linux; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00;)AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/18.0.1025 Mobile Safari/537.36 hap/1040/huawei com.huawei.fastapp/1.1.2.300 com.ss.android.article.quickapp/2.0.0 ({"extra":{"original":{"packageName":"com.huawei.appmarket","type":"url"},"scene":"dialog"},"packageName":"com.huawei.android.launcher","type":"shortcut"})'
}


def init():
    for i in range(20):
        ascp = public.get_ASCP()
        form = {
            'ac': 'wap',
            'format': 'json_raw',
            'min_behot_time': int(time.time()),
            'as': ascp[0],
            'enable_stick': 'false',
            'tag': 'video',
            'cp': ascp[1],
        }
        for item in public.request_data(LIST_API, cookie=COOKIE, header=HEADER, params=form).get('data', []):
            video = {}
            video['_id'] = public.format_id(item.get('title'))
            video['title'] = item.get('title')
            video['from'] = '今日头条'
            video['pic'] = item.get('large_image_url')
            r, s = public.get_rs(item.get('video_id'))
            video['url'] = base64.b64decode(public.request_data(
                DETAIL_API + item.get('video_id'), params={'r': r, 's': s}, header=HEADER).get('data').get('video_list').get('video_1').get('main_url').encode('utf-8')).decode('utf-8')
            video['timestamp'] = int(time.time())
            public.save_data(video, DB_NAME)


if __name__ == "__main__":
    init()
