'''
file_name:getFileByte.py
app:all
funtion:get file byte
include:
 1.function:getFile:get file byte
data:2018/09/11
author:Ricky
'''

'''
function：get file bytes
parameters@filePath: file path
return@文件流
data:2018/09/11
author:Ricky
'''


def getFile(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


'''
function：store file
parameters@filePath: file path@file:the byte of file
return@status
data:2018/09/11
author:Ricky
'''


def setFile(filePath, file):
    try:
        with open(filePath, 'wb+') as f:
            for chrunk in file.chunks():
                f.write(chrunk)
        f.close()
        return 0
    except:
        return 1
