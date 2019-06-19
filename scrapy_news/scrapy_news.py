import news_baidu
import news_fenghuang
import news_pengpai
import news_sina
import news_tencent
import news_toutiao
import news_wangyi
import time
import multiprocessing


def scrapy():
    while True:
        process1 = multiprocessing.Process(
            target=news_baidu.init)
        process2 = multiprocessing.Process(
            target=news_fenghuang.init)
        process3 = multiprocessing.Process(
            target=news_pengpai.init)
        process4 = multiprocessing.Process(
            target=news_sina.init)
        process5 = multiprocessing.Process(
            target=news_tencent.init)
        process6 = multiprocessing.Process(
            target=news_toutiao.init)
        process7 = multiprocessing.Process(
            target=news_wangyi.init)
        process1.start()
        process2.start()
        process3.start()
        process4.start()
        process5.start()
        process6.start()
        process7.start()
        time.sleep(60 * 60)


if __name__ == "__main__":
    scrapy()
