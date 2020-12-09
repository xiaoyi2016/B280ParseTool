import pandas as pd
import time
import os
import struct
from ParseCommon import *

# 解释一个睡眠拉取数据时的临时文件，添加到excel文件中
#

# 睡眠数据1个分包文件中，数码数据的长度
SLEEP_DATA_LEN  = 480

# 时间戳和状态数据长度
INDEX_RECORD_ONE = '<IH2x'

# 睡眠数据
INDEX_RECORD_TWO = '<B'

def parseOneRecord(fd,outfile,baseTime,statusLen,index):
    timeLocal = time.localtime(int(baseTime))
    dtTime = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

    print('时间戳：' + dtTime + '  数据长度：' + str(statusLen))

    for i in range(1,statusLen):
        record = fd.read(1)
        sleepStatus = struct.unpack(INDEX_RECORD_TWO, record)

        if index == 0:
            dic = {
                TITLE_TIMESTAMP: [baseTime],
                TITLE_DATETIME: [dtTime],
                TITLE_SLEEP_DATA_LEN: [statusLen],
                TITLE_SLEEP_STATUS: [sleepStatus]
            }
            df = pd.DataFrame(dic)
            df.to_csv(outfile, index=None, mode='a')
        else:
            dic = {
                TITLE_TIMESTAMP: [baseTime],
                TITLE_DATETIME: [dtTime],
                TITLE_SLEEP_DATA_LEN: [''],
                TITLE_SLEEP_STATUS: [sleepStatus]
            }
            df = pd.DataFrame(dic)
            df.to_csv(outfile, index=None, header=0, mode='a')

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseSleepTmp(inputfile,outfile):
    print('需要转换的文件:' + inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    datetimeIndex = len(datetime) - 2

    print('基础日期：' + datetime[datetimeIndex])
    index = 0
    currentTime = time.time()

    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)


    with open(inputfile,'rb') as fd:
        record = fd.read(8)
        while len(record)>0 :
            timeStamp, statusLen = struct.unpack(INDEX_RECORD_ONE, record)
            record = fd.read(SLEEP_DATA_LEN)
            parseOneRecord(fd,outfile, timeStamp,statusLen,index)
            record = fd.read(8)
            index = index + 1

    print (outfile+" 转换结束")