import pandas as pd
from ParseCommon import *
import os
import time

# 解释一个 每日睡眠 数据，添加到excel文件中
# 目前睡眠的存储结构是
#  1 byte  spo min 最小睡眠血氧
#  1 byte  spo max 最大睡眠血氧
#  n byte  睡眠状态  一天的数据最大在 24 * 60 /4   1分钟打点1次  1个字节可用存储4次打点数据

def writeDataToFile(status,outfile,timestamp):
    dic = {TITLE_BASE_DT: [timestamp],
           TITLE_SLEEP_SPO_MIN: [''],
           TITLE_SLEEP_SPO_MAX: [''],
           TITLE_SLEEP_STATUS: [status]
           }

    df = pd.DataFrame(dic)
    df.to_csv(outfile,index=False,mode='a',header=0)

def parseOneRecord(record,outfile,basetime):
    bytebufT = byte_buffer_t()
    byte_buffer_create(bytebufT, record, len(record))
    sleepStatus = byte_buffer_get_byte(bytebufT, 0)

    oneStatus = sleepStatus & 0x03
    timestamp = int(basetime)
    timeLocal = time.localtime(timestamp)
    dttime = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    writeDataToFile(oneStatus,outfile,dttime)

    oneStatus = (sleepStatus>>2) & 0x03
    timestamp = int(basetime) + 60
    timeLocal = time.localtime(timestamp)
    dttime = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    writeDataToFile(oneStatus, outfile,dttime)

    oneStatus = (sleepStatus >> 4) & 0x03
    timestamp = int(basetime) + 120
    timeLocal = time.localtime(timestamp)
    dttime = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    writeDataToFile(oneStatus, outfile,dttime)

    oneStatus = (sleepStatus >> 6) & 0x03
    timestamp = int(basetime) + 180
    timeLocal = time.localtime(timestamp)
    dttime = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    writeDataToFile(oneStatus, outfile,dttime)

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseDailySleep(inputfile,outfile):
    print ('需要转换的文件:'+inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    datetimeIndex = len(datetime) - 2
    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile
    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    with open(inputfile,'rb') as fd:
        record = fd.read(2)

        # 创建结构体对象
        bytebufT = byte_buffer_t()
        byte_buffer_create(bytebufT, record, len(record))

        sleepSpoMin = byte_buffer_get_byte(bytebufT, 0)
        sleepSpoMax = byte_buffer_get_byte(bytebufT,0)

        del bytebufT

        dic = {TITLE_BASE_DT: [''],
               TITLE_SLEEP_SPO_MIN: [sleepSpoMin],
               TITLE_SLEEP_SPO_MAX: [sleepSpoMax],
               TITLE_SLEEP_STATUS: ['']
        }

        df = pd.DataFrame(dic)
        df.to_csv(outfile, index=None, mode='a')

        baseTimeStamp = int(datetime[datetimeIndex]) - 4*3600

        record = fd.read(1)
        while len(record) > 0:
            parseOneRecord(record, outfile, baseTimeStamp)
            baseTimeStamp = baseTimeStamp + 240
            record = fd.read(1)

    print (outfile+" 转换结束")