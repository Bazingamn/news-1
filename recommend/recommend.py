from news import settings
import pymysql
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS
from pyspark.sql import SparkSession
import time
import sys
import os
os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"
sys.path.append('..')
sc = SparkContext('local[*]')
sc.setLogLevel('ERROR')
sqlContext = SQLContext(sc)
spark = SparkSession.builder.appName('test').getOrCreate()
url = "jdbc:mysql://120.77.144.237:3306/news?user=news&password=1107786871"
db = pymysql.connect(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['USER'],
                     settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['NAME'], charset='utf8mb4')
cursor = db.cursor()


def save(data):
    for item in data.collect():
        df = spark.createDataFrame(item[1])
        df.write.jdbc(url=url, mode="append", table="T_RECOMMEND",
                      properties={"driver": "com.mysql.jdbc.Driver"})
    print('保存成功')


def clear_data():
    cursor.execute('truncate T_RECOMMEND;')
    db.commit()
    print('已清空推荐表')


def init():
    while True:
        try:
            dataframe_mysql = sqlContext.read.format("jdbc").option("url", "jdbc:mysql://localhost/db?useSSL=false").options(
                url="jdbc:mysql://120.77.144.237:3306/news", dbtable="T_BROWSE_REC", user="news", password="1107786871").load()
            dataframe_mysql = dataframe_mysql.select('USER_ID', 'NEWS_ID').rdd.map(
                lambda x: ((x.USER_ID, x.NEWS_ID), 1))
            data = dataframe_mysql.reduceByKey(lambda a, b: a +
                                               b).map(lambda x: (x[0][0], x[0][1], x[1]))
            model = ALS.train(data, 10, 10, 0.01)
            res = model.recommendProductsForUsers(500)
            clear_data()
            save(res)
            time.sleep(60 * 60)
        except Exception as e:
            print(e)
            time.sleep(60 * 60)
            continue


if __name__ == "__main__":
    init()
