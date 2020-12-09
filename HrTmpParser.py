import pandas as pd
from ParseCommon import *
import os
import time

# 解释一个日常心率拉取数据时的临时文件，添加到excel文件中
#

RECORD_SIZE = 8

def parseOneRecord(record,outfile,index):
    # 创建结构体对象
    bytebufT = byte_buffer_t()
    byte_buffer_create(bytebufT, record, len(record))

    # 相对文件记录起始地址的时间戳偏移值
    timestamp = byte_buffer_get_int(bytebufT, 0)
    timeLocal = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)
    heartrate = byte_buffer_get_byte(bytebufT, 0)
    type = byte_buffer_get_byte(bytebufT, 0)

    dic = {TITLE_TIMESTAMP: [timestamp],
           TITLE_DATETIME: [ dt ],
           TITLE_HR: [heartrate],
           TITLE_TYPE: [type]
           }

    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile, index=None, mode='a')
    else:
        df.to_csv(outfile, index=None, header=0, mode='a')

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseHrTmp(inputfile,outfile):
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
    with open(inputfile,'rb') as fd:
        record = fd.read(RECORD_SIZE)
        while len(record) > 0:
            # df = pd.read_excel(outfile, header=None)
            parseOneRecord(record,outfile,index)
            record = fd.read(RECORD_SIZE)
            index = index + 1
    print (outfile+" 转换结束")