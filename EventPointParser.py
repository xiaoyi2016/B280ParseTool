import pandas as pd
from ParseCommon import *
import time
import os
import struct
from collections import namedtuple

def parseEPIndexOneRecord(record,outfile,index):
    timeStamp,filename = struct.unpack(EVENTPOINT_INDEX_RECORD_ONE, record)

    timeLocal = time.localtime(int(timeStamp))
    # 转换成新的时间格式
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    # b' 标示byte类型  和str类型转换
    # str.encode('utf-8') sb = bytes(s, encoding = "utf8")
    # bytes.decode('utf-8') bs = str(b, encoding = "utf8")

    dic = {
           TITLE_TIMESTAMP:[ timeStamp ],
           TITLE_DATETIME: [ dt ],
           TITLE_EP_FILENAME: [ str(filename, encoding = "GBK") ],
          }


    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a',encoding='utf_8_sig')
    else:
        df.to_csv(outfile,index=False,mode='a',encoding='utf_8_sig',header=0)


def parseEPDataOneRecord(record,outfile,index):
    timeStamp,serviceID,eventID,eventKeyId,value = struct.unpack(EVENTPOINT_RECORD_ONE, record)

    timeLocal = time.localtime(int(timeStamp))
    # 转换成新的时间格式
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    # b' 标示byte类型  和str类型转换
    # str.encode('utf-8') sb = bytes(s, encoding = "utf8")
    # bytes.decode('utf-8') bs = str(b, encoding = "utf8")
    print('eventkeyid: '+ eventKeyId.decode('utf-8') )
    print('value: ' + value.decode('utf-8'))

    dic = {
           TITLE_TIMESTAMP:[ timeStamp ],
           TITLE_DATETIME: [ dt ],
           TITLE_EP_SERVICEID: [ serviceID.decode('utf-8') ],
           TITLE_EP_EVENTID: [ eventID.decode('utf-8') ],
           TITLE_EP_KEYID: [eventKeyId.decode('utf-8')],
           TITLE_EP_VALUE: [value.decode('utf-8')],
          }


    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a',encoding='utf_8_sig')
    else:
        df.to_csv(outfile,index=False,mode='a',encoding='utf_8_sig',header=0)

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseEventPointIndex(inputfile,outfile):
    print ('需要转换的文件:'+inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    datetimeIndex = len(datetime) - 2

    print ('基础日期：'+datetime[datetimeIndex])
    index = 0

    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    recordSize = struct.calcsize(EVENTPOINT_INDEX_RECORD_ONE)
    print('recordsize:' + str(recordSize))

    with open(inputfile,'rb') as fd:
        readbyte = fd.read(recordSize)
        print('实际读取的字节数：' + str(len(readbyte)))

        while len(readbyte) == recordSize:
            parseEPIndexOneRecord(readbyte, outfile, index)
            readbyte = fd.read(recordSize)
            print('实际读取的字节数：' + str(len(readbyte)))
            index = index + 1
    print ('转换后文件保存：'+ outfile)



# 解析埋点数据文件
def parseEventPointData(inputfile,outfile):
    print ('需要转换的文件:'+inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    datetimeIndex = len(datetime) - 2

    print ('基础日期：'+datetime[datetimeIndex])
    index = 0

    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    recordSize = struct.calcsize(EVENTPOINT_RECORD_ONE)
    print('recordsize:' + str(recordSize))

    with open(inputfile,'rb') as fd:
        readbyte = fd.read(recordSize)
        print('实际读取的字节数：' + str(len(readbyte)))

        while len(readbyte) == recordSize:
            parseEPDataOneRecord(readbyte, outfile, index)
            readbyte = fd.read(recordSize)
            print('实际读取的字节数：' + str(len(readbyte)))
            index = index + 1
    print ('转换后文件保存：'+ outfile)