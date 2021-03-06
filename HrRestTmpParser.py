import pandas as pd
from ParseCommon import *

# 解释一个静息心率拉取数据时的临时文件，添加到excel文件中
#

RECORD_SIZE = 8

def parseOneRecord(record):
    # 创建结构体对象
    bytebufT = byte_buffer_t()
    byte_buffer_create(bytebufT, record, len(record))

    # 相对文件记录起始地址的时间戳偏移值
    timestamp = byte_buffer_get_int(bytebufT, 0)
    heartrate = byte_buffer_get_byte(bytebufT, 0)

    dic = {TITLE_TIMESTAMP: [timestamp],
           TITLE_HR: [heartrate]
           }

    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile, index=None, mode='a')
    else:
        df.to_csv(outfile, index=None, header=0, mode='a')

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseHrRstTmp(inputfile,outfile):
    print ('需要转换的文件:'+inputfile)
    datetime = inputfile.split('_')
    index = 0
    with open(inputfile,'rb') as fd:
        record = fd.read(RECORD_SIZE)
    print (outfile+" 转换结束")