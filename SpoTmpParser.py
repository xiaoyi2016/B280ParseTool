import pandas as pd
from ParseCommon import *
import time
import os
import struct
from collections import namedtuple

# 时间戳异常的数据的序列值
timeErrIndex = 0

# 血氧索引 数据格式
SPO_RECORD_ONE = '<2I2B2x'

# 解释一个 运动报告 数据，添加到excel文件中
#
def saveTimeErrorData(outfile,index,content):
    df = pd.DataFrame(content)
    if index == 0:
        df.to_csv(EXCEPTION_TIME_ERROR_EXT+outfile,index=False,mode='a')
    else:
        df.to_csv(EXCEPTION_TIME_ERROR_EXT+outfile,index=False,mode='a',header=0)

def parseOneRecord(record,outfile,index):
    timeStamp,interval,spo2,reliability = struct.unpack(SPO_RECORD_ONE, record)

    timeLocal = time.localtime(int(timeStamp))

    # 转换成新的时间格式
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

    dic = {TITLE_TIMESTAMP:[ timeStamp ],
           TITLE_DATETIME: [ dt ],
           TITLE_SPO2: [spo2],
           TITLE_SPO2_GAP: [interval],
           TITLE_SPO2_QUALITY: [ reliability ],
            }


    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a')
    else:
        df.to_csv(outfile,index=False,mode='a',header=0)

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseSpoTmp(inputfile,outfile):
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

    recordSize = struct.calcsize(SPO_RECORD_ONE)
    print('recordsize:' + str(recordSize))

    with open(inputfile,'rb') as fd:
        readbyte = fd.read(recordSize)

        while len(readbyte)>0 :
            parseOneRecord(readbyte, outfile, index)
            readbyte = fd.read(recordSize)
            index = index + 1
    print ('转换后文件保存：'+ outfile)