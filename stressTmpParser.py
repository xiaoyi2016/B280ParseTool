import pandas as pd
from ParseCommon import *
import os
import time
import struct

# 解析压力拉取数据时的临时文件，添加到excel文件中
#
STRESS_RECORD_ONE = '<IB3xIB3x'

def parseOneRecord(record,outfile,index):
    timeStamp, stress, reliability,type = struct.unpack(STRESS_RECORD_ONE, record)

    timeLocal = time.localtime(int(timeStamp))

    # 转换成新的时间格式
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

    dic = {TITLE_TIMESTAMP: [timeStamp],
           TITLE_DATETIME: [dt],
           TITLE_STRESS: [stress],
           TITLE_TYPE: [type],
           TITLE_QUALITY: [reliability],
           }

    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile, index=False, mode='a')
    else:
        df.to_csv(outfile, index=False, mode='a', header=0)

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseStressTmp(inputfile,outfile):
    print ('需要转换的文件:'+inputfile)
    ( path , filename ) = os.path.split(inputfile)
    print ("路径："+path)
    print ("文件名："+filename)
    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    index = 0
    recordSize = struct.calcsize(STRESS_RECORD_ONE)
    print('recordsize:' + str(recordSize))

    with open(inputfile,'rb') as fd:
        record = fd.read(recordSize)
        while len(record) > 0:
            parseOneRecord(record,outfile,index)
            record = fd.read(recordSize)
            index = index + 1
    print (outfile+" 转换结束")