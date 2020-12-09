import pandas as pd
from ParseCommon import *
import time
import os
import struct
from collections import namedtuple

# 运动记录打点数据格式

# 解释运动记录数据，添加到excel文件中

# 解析1个record的游泳数据
def parseOneSportSwimRecord(record,outfile,datetime,index,currentTime):
    # 创建结构体对象
    hasData,timeStamp,distanceInc,hr,step,altitude,calories,stepfre = struct.unpack(SPORT_RECORD_ONE,record)

    dic = {TITLE_TIMESTAMP:[ timeStamp ],
           TITLE_DIST: [ distanceInc ],
            }


    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a')
    else:
        df.to_csv(outfile,index=False,mode='a',header=0)



# 解析1个record的非游泳数据
def parseOneSportRecord(record,outfile,datetime,index,currentTime):
    # 创建结构体对象
    hasData,timeStamp,distanceInc,hr,step,altitude,calories,stepfre = struct.unpack(SPORT_REC_RECORD_ONE,record)

    dic = {TITLE_TIMESTAMP:[ timeStamp ],
           TITLE_DIST: [ distanceInc ],
            }


    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a')
    else:
        df.to_csv(outfile,index=False,mode='a',header=0)


# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseSportRecord(inputfile,outfile):
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

    recordSize = struct.calcsize(SPORT_REC_RECORD_ONE)
    print('recordsize:' + str(recordSize))

    with open(inputfile,'rb') as fd:
        readbyte = fd.read(recordSize)
        parseOneSportRecord(readbyte, outfile, datetime[datetimeIndex], index, currentTime)
        #while len(readbyte)>0 :
        #    parseOneSportRecord(readbyte,outfile,datetime[0],index,currentTime)
        #    readbyte = fd.read(DAILY_RECORD_SIZE)
         #   index = index + 1
    print ('转换后文件保存：'+ outfile)
