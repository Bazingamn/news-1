import time
import public
API = 'http://api.k.sohu.com/api/videotab/getVideoListWechat.go?channelId=30000&carrier=&mainFocalId=0&focusPosition=1&rr=1&openId=NTgxMzI2NTA4Njk5NDcxNDY1MQ%3D%3D&u=113&net=wifi&rc=1&recomtype=0&lc='
DB_NAME = 'video'


def init():
    for lc in range(20):
        for item in public.request_data(API + str(lc)).get('data').get('videoList', []):
            video = {}
            video['_id'] = public.format_id(item.get('title'))
            video['title'] = item.get('title')
            video['from'] = '搜狐视频'
            video['pic'] = item.get('tvPic')
            video['url'] = item.get('playUrl')
            video['timestamp'] = int(time.time())
            public.save_data(video, DB_NAME)


if __name__ == "__main__":
    init()
