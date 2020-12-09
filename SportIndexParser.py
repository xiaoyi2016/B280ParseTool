import pandas as pd
from ParseCommon import *
import time
import os
import struct
from collections import namedtuple

# 时间戳异常的数据的序列值
timeErrIndex = 0

# 运动索引 数据格式
SPORT_INDEX_RECORD_ONE = '<2H3I33s3x'

# 解释一个 运动报告 数据，添加到excel文件中
#
def saveTimeErrorData(outfile,index,content):
    df = pd.DataFrame(content)
    if index == 0:
        df.to_csv(EXCEPTION_TIME_ERROR_EXT+outfile,index=False,mode='a')
    else:
        df.to_csv(EXCEPTION_TIME_ERROR_EXT+outfile,index=False,mode='a',header=0)

def parseOneRecord(record,outfile,index):
    version,sportType,timeStamp,timeTick,timeStampEnd,stringID = struct.unpack(SPORT_INDEX_RECORD_ONE, record)

    timeLocal = time.localtime(int(timeStamp))
    timeEndLocal = time.localtime(int(timeStampEnd))
    # 转换成新的时间格式
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    dtEnd = time.strftime("%Y-%m-%d-%H-%M-%S", timeEndLocal)

    # b' 标示byte类型  和str类型转换
    # str.encode('utf-8')
    # bytes.decode('utf-8')

    dic = {
           TITLE_TIMESTAMP:[ timeStamp ],
           TITLE_DATETIME: [ dt ],
           TITLE_TYPE: [sportType],
           TITLE_TYPE_NAME:[ getSportName(sportType) ],
           TITLE_TIMESTAMP_END: [ timeStampEnd ],
           TITILE_END_DATETIME: [ dtEnd ],
           TITLE_SPORTID: [ stringID.decode('GBK') ],
           TITLE_VERSION: [ version ]
            }


    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a')
    else:
        df.to_csv(outfile,index=False,mode='a',header=0)

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseSportIndex(inputfile,outfile):
    print ('需要转换的文件:'+inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    datetimeIndex = len(datetime) - 2

    print ('基础日期：'+datetime[datetimeIndex])
    index = 0
    currentTime = time.time()

    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    recordSize = struct.calcsize(SPORT_INDEX_RECORD_ONE)
    print('recordsize:' + str(recordSize))

    with open(inputfile,'rb') as fd:
        readbyte = fd.read(recordSize)
        print('实际读取的字节数：' + str(len(readbyte)))

        while len(readbyte) == recordSize:
            parseOneRecord(readbyte, outfile, index)
            readbyte = fd.read(recordSize)
            print('实际读取的字节数：' + str(len(readbyte)))
            index = index + 1
    print ('转换后文件保存：'+ outfile)