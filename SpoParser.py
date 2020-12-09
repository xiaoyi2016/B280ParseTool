import pandas as pd
from ParseCommon import *
import time
import os
import struct
from collections import namedtuple
from SpoIndexParser import parseSpoIndex

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
    print('spo值:'+str(spo2))
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

    # 普通血氧
    if interval == 255:
        (path, filename) = os.path.split(outfile)
        newoutfile = path + '\\' + 'normal_' + filename
    else:
        newoutfile = outfile

    if index == 0:
        df.to_csv(newoutfile,index=False,mode='a')
    else:
        df.to_csv(newoutfile,index=False,mode='a',header=0)

# inputfile: 需要转换的文件 完整路径
#          1 如果传递完整的文件名 ，表示解析单个文件
#          2 如果传递的是文件路径 ，表示解析目录下的所有文件
# outfile:   转换后的文件 完整路径
def parseSpo(inputfile):
    print ('需要转换的文件:'+inputfile)
    path = ''
    filename = ''
    (path, filename) = os.path.split(inputfile)
    index = 0
    print('路径'+path)
    print('文件名'+filename)

    # 转换成localtime
    timeLocal = time.localtime(time.time())
    # 转换成新的时间格式(2016-05-05-20-28-54)
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    recordSize = struct.calcsize(SPO_RECORD_ONE)
    print('recordsize:' + str(recordSize))
    filelist = os.listdir(path)
    print(filelist)

    outpath = path + TRANSLATED_FILE_DIR

    isExist = os.path.exists(outpath)
    if not isExist:
        os.makedirs(outpath)

    if len(filename) != 0:
        outfile = outpath + '\\' + SPO_OUT_FILENAME_PRE + filename + '_' + dt + OUT_FILE_EXT
        with open(inputfile,'rb') as fd:
            readbyte = fd.read(recordSize)

            while len(readbyte)>0 :
                parseOneRecord(readbyte, outfile, index)
                readbyte = fd.read(recordSize)
                index = index + 1
    else:
        for nameindex in range(0,len(filelist)):
            # 如果是目录 跳过
            if os.path.isdir(filelist[nameindex]):
                continue

            # 如果是index0.spo 索引文件 跳过
            if len(filelist[nameindex].split('_')) < 2:
                continue
            index = 0
            newfilename = path+'\\'+filelist[nameindex]
            outfile = outpath + '\\' + SPO_OUT_FILENAME_PRE + filelist[nameindex] + '_' + dt + OUT_FILE_EXT
            print('新文件  ' + newfilename)
            print('输出文件名：' + outfile)
            with open(newfilename, 'rb') as fd:
                readbyte = fd.read(recordSize)

                while len(readbyte) > 0:
                    parseOneRecord(readbyte, outfile, index)
                    readbyte = fd.read(recordSize)
                    index = index + 1

    print ('转换后文件保存：'+ outfile)