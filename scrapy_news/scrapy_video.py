import video_baidu
import video_haotu
import video_kanjian
import video_lishipin
import video_pengpai
import video_sina
import video_sohu
import video_toutiao
import time
import multiprocessing


def scrapy():
    while True:
        process1 = multiprocessing.Process(
            target=video_baidu.init)
        process2 = multiprocessing.Process(
            target=video_haotu.init)
        process3 = multiprocessing.Process(
            target=video_kanjian.init)
        process4 = multiprocessing.Process(
            target=video_lishipin.init)
        process5 = multiprocessing.Process(
            target=video_pengpai.init)
        process6 = multiprocessing.Process(
            target=video_sina.init)
        process7 = multiprocessing.Process(
            target=video_sohu.init)
        process8 = multiprocessing.Process(
            target=video_toutiao.init)
        process1.start()
        process2.start()
        process3.start()
        process4.start()
        process5.start()
        process6.start()
        process7.start()
        process8.start()
        time.sleep(60 * 60)


if __name__ == "__main__":
    scrapy()
