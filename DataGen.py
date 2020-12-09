#
# 1. 生成运动和健康的数据和索引文件，用于模拟压测
# 2. 生成埋点文件的数据和索引文件，用于压测
#

import sys
import time
import os
import random
from DataGenConfig import  *
from ParseCommon import *
import struct

# 更新血氧索引文件
def updateHealthSpo2Index(startTime,endTime,type,filename):
    print('索引文件：'+ filename)
    fd = open(filename, 'ab')
    if type == 255:
        type = 1
    else:
        type = 2

    data = struct.pack(SPO_INDEX_RECORD_ONE, startTime, endTime, type)
    fd.write(data)
    fd.close()


def genHealthSpo2Record(startTime,endTime,interval,outPath):
    filename = outPath + '\\' + "{:0>8x}_".format(startTime) + HEALTH_SPO_DATA_VERSION_NUM + HEALTH_SPO_FILE_EXT
    indexFilename = outPath + '\\' + HEALTH_SPO_INDEX_EXT
    updateHealthSpo2Index(startTime,endTime,interval,indexFilename)
    print('生成的数据文件：'+filename)
    fd = open(filename, 'wb')

    while startTime <= endTime:
        # spo2 = random.choice(HEALTH_SPO2_VALUE)
        spo2 = random.randint(HEALTH_SPO2_MIN, HEALTH_SPO2_MAX)
        reliability = random.randint(0, 5)
        data = struct.pack(SPO_RECORD_ONE, startTime, interval, spo2, reliability)
        fd.write(data)
        if interval == 255:
          startTime = startTime + random.randint(1, 5)
        else:
          startTime = startTime + random.randint(1, 50)

    fd.close()


def genHealthSpo2(outPath):
    print('文件保存到:'+outPath)

    timeArray = time.strptime(HEALTH_TIMESTAMP_END,"%Y-%m-%d %H:%M:%S")
    endTime = int(time.mktime(timeArray))
    curTime = time.time()

    # 如果结束时间超过了当前时间，将当前时间设置为结束时间
    if endTime > curTime:
        endTime = curTime

    startTime = endTime - HEALTH_TIMESTAMP_MAX_DAY * 24 *3600

    print('基础时间：'+ str(startTime) + ' 最大天数：'+ str(HEALTH_TIMESTAMP_MAX_DAY))
    interval = random.randint(HEALTH_SPO_TYPE_MIN, HEALTH_SPO_TYPE_MAX)

    recordStartTime = startTime +  random.randint(HEALTH_SPO_GAP_TIME_MIN,HEALTH_SPO_GAP_TIME_MAX)
    if interval == 255:
      recordEndTime   = recordStartTime + random.randint(HEALTH_SPO_NORMAL_TIME_MIN,HEALTH_SPO_NORMAL_TIME_MAX)
    else:
      recordEndTime = recordStartTime + random.randint(HEALTH_SPO_SLEEP_TIME_MIN, HEALTH_SPO_SLEEP_TIME_MAX)

    print('开始时间：' +  str(recordStartTime) + ' 结束时间：'+str(recordEndTime))
    while recordEndTime < endTime:
        genHealthSpo2Record(recordStartTime, recordEndTime,interval,outPath)
        interval = random.randint(HEALTH_SPO_TYPE_MIN, HEALTH_SPO_TYPE_MAX)
        recordStartTime = recordEndTime + random.randint(HEALTH_SPO_GAP_TIME_MIN, HEALTH_SPO_GAP_TIME_MAX)
        if interval == 255:
            recordEndTime = recordStartTime + random.randint(HEALTH_SPO_NORMAL_TIME_MIN, HEALTH_SPO_NORMAL_TIME_MAX)
        else:
            recordEndTime = recordStartTime + random.randint(HEALTH_SPO_SLEEP_TIME_MIN, HEALTH_SPO_SLEEP_TIME_MAX)
        print('开始时间：' + str(recordStartTime) + ' 结束时间：' + str(recordEndTime))


# 更新埋点索引文件
def updateEventPointIndex(startTime,epFileName,filename):
    print('索引文件：'+ filename)
    fd = open(filename, 'ab')
    data = struct.pack(EVENTPOINT_INDEX_RECORD_ONE, startTime, bytes(epFileName, encoding = "utf8"))
    fd.write(data)
    fd.close()

def genEventPointRecord(startTime, endTime, outPath):
    filename = "ep_{:0>8x}.evt".format(startTime)
    fullName = outPath + '\\' + filename
    indexFilename = outPath + '\\' + 'ep_index.txt'
    updateEventPointIndex(startTime, filename, indexFilename)
    print('生成的数据文件：' + fullName)
    fd = open(fullName, 'wb')

    while startTime <= endTime:
        serviceID = '2018703'
        eventID = '1026002'
        keyID = 'testID'
        value = 'test'
        data = struct.pack(EVENTPOINT_RECORD_ONE, startTime,serviceID.encode('utf-8'),eventID.encode('utf-8'),keyID.encode('utf-8'),value.encode('utf-8'))

        fd.write(data)
        startTime = startTime + random.randint(1, 5)

    fd.close()

# 生成埋点数据文件
def genEventPointData(outPath):
    timeArray = time.strptime(HEALTH_TIMESTAMP_END,"%Y-%m-%d %H:%M:%S")
    endTime = int(time.mktime(timeArray))
    curTime = time.time()

    # 如果结束时间超过了当前时间，将当前时间设置为结束时间
    if endTime > curTime:
        endTime = curTime

    startTime = endTime - EP_TIMESTAMP_DAY * 24 * 3600

    print('基础时间：' + str(startTime) + ' 最大天数：' + str(EP_TIMESTAMP_DAY))

    recordStartTime = startTime + random.randint(EP_DATA_GAP_TIME_MIN, EP_DATA_GAP_TIME_MAX)
    recordEndTime = recordStartTime + random.randint(EP_ONE_FILE_TIME_MIN, EP_ONE_FILE_TIME_MAX)

    print('开始时间：' + str(recordStartTime) + ' 结束时间：' + str(recordEndTime))

    while recordEndTime < endTime:
        genEventPointRecord(recordStartTime, recordEndTime, outPath)
        recordStartTime = recordEndTime + random.randint(EP_DATA_GAP_TIME_MIN, EP_DATA_GAP_TIME_MAX)
        recordEndTime = recordStartTime + random.randint(EP_ONE_FILE_TIME_MIN, EP_ONE_FILE_TIME_MAX)
        print('开始时间：' + str(recordStartTime) + ' 结束时间：' + str(recordEndTime))


def _mainProcess():
    if len(sys.argv) >= 3:
        i = sys.argv[1]
        path = sys.argv[2]
        print (path)
    else:
        print('参数错误')
        return

    for i in sys.argv:
        if i == TRANSLATE_TYPE_HEALTH_SPO:
            print('生成血氧模拟测试数据:')
            genHealthSpo2(path)
        elif i == TRANSLATE_TYPE_EVENTPOINT:
            print('生成埋点模拟测试数据:')
            genEventPointData(path)



if __name__ == '__main__':
    _mainProcess()