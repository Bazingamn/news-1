"""
file_name:fileOperation.py
app:Libs
funtion:operate the file of Tencent cos file
include:
 1.function:up@upload file to Tencent cos
 2.function:delete@delete the file on Tencent cos
data:2018/09/06
author:Ricky
"""

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import json
import logging
import re
from django.conf import settings

'''
the client of cos
'''
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
config = CosConfig(Region=settings.REGION, SecretId=settings.SECRETID,
                   SecretKey=settings.SECRETKEY, Token=settings.TOKEN, Scheme=settings.SCHEMA)
# 2. 获取客户端对象
client = CosS3Client(config)

'''
function：upload file to Tencent cos
parameters@file:the object of file@file_name:the upload path and file name of file
return@str:the url of file
data:2018/09/06
author:Ricky
'''


def up(file, file_name):
    response = client.put_object(Bucket='newsapp-1254170634', Body=file, Key=file_name,
                                 StorageClass='STANDARD', ContentType='text/html; charset=utf-8')
    return "https://newsapp-1254170634.cos.ap-chengdu.myqcloud.com/" + file_name


'''
function：delete file on Tencent cos
parameters@filePath:the file's path on Tencent cos
return@str:ok
data:2018/09/06
author:Ricky
'''


def delete(filePath):
    try:
        filePath = ('/'.join(filePath.split('/')[3:]))
        response = client.delete_object(
            Bucket='newsapp-1254170634', Key=filePath)
        return True
    except:
        return False
