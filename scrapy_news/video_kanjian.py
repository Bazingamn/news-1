import time
import public
LIST_API = 'https://apps.zhonglanmedia.com/h5app/findRecommendDailyLearningPage.do'
DETAIL_API = 'https://apps.zhonglanmedia.com/h5app/findVideoDetail.do'
DB_NAME = 'video'
HEADER = {
    'Access': 'huawei',
    'user-agent': 'Mozilla/5.0 (Linux; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00;)AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/18.0.1025 Mobile Safari/537.36 hap/1040/huawei com.huawei.fastapp/1.1.2.300 com.application.kanjian/3.0.6 ({"packageName":"unknown","type":"unknown"})'
}


def init():
    for i in range(20):
        form = {
            'rtype': 0,
            'pageNum': i,
            'pageSize': 10
        }
        for item in public.request_data(LIST_API, params=form, header=HEADER, method='POST').get('page').get('result', []):
            video = {}
            video['_id'] = public.format_id(item.get('title'))
            video['title'] = item.get('title')
            video['from'] = '看鉴视频'
            video['pic'] = item.get('image')
            video['url'] = public.request_data(
                DETAIL_API, params={'videoId': item['rid']}, header=HEADER, method='POST').get('upyunVideos')[0].get('playurl')
            video['timestamp'] = int(time.time())
            public.save_data(video, DB_NAME)


if __name__ == "__main__":
    init()
