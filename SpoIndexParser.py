import pandas as pd
from ParseCommon import *
import time
import os
import struct
from collections import namedtuple

# 解释一个 运动报告 数据，添加到excel文件中
#
def saveTimeErrorData(outfile,index,content):
    df = pd.DataFrame(content)
    if index == 0:
        df.to_csv(EXCEPTION_TIME_ERROR_EXT+outfile,index=False,mode='a')
    else:
        df.to_csv(EXCEPTION_TIME_ERROR_EXT+outfile,index=False,mode='a',header=0)

def parseOneRecord(record,outfile,index):
    timeStamp,endTimeStamp,type = struct.unpack(SPO_INDEX_RECORD_ONE, record)

    timeLocal = time.localtime(int(timeStamp))
    timeLocal2 = time.localtime(int(endTimeStamp))

    # 转换成新的时间格式
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    dt2 = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal2)

    if type == 1:
        spoType = TITLE_SPO_NORMAL
    elif type == 2:
        spoType = TITLE_SPO_SLEEP
    else:
        spoType = TITLE_SPO_UNKNOWN

    dic = {TITLE_TIMESTAMP:[ timeStamp ],
           TITLE_TIMESTAMP_HEX: [ "{:>08x}".format(int(timeStamp))],
           TITLE_DATETIME: [ dt ],
           TITLE_TIMESTAMP_END: [endTimeStamp],
           TITILE_END_DATETIME: [dt2],
           TITLE_SPO_TYPE: [ spoType ],
            }


    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a')
    else:
        df.to_csv(outfile,index=False,mode='a',header=0)

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseSpoIndex(inputfile,outfile):
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

    recordSize = struct.calcsize(SPO_INDEX_RECORD_ONE)
    print('recordsize:' + str(recordSize))

    with open(inputfile,'rb') as fd:
        readbyte = fd.read(recordSize)

        while len(readbyte)>0 :
            parseOneRecord(readbyte, outfile, index)
            readbyte = fd.read(recordSize)
            index = index + 1
    print ('转换后文件保存：'+ outfile)