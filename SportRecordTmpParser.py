import json

import pandas as pd
from ParseCommon import *
import time
import os

#  每日活动记录的单个数据结构的大小
DAILY_RECORD_SIZE = 13

# 时间戳异常的数据的序列值
timeErrIndex = 0

# 解释一个每日活动记录数据，添加到excel文件中
#
def saveTimeErrorData(outfile,index,content):
    df = pd.DataFrame(content)
    if index == 0:
        df.to_csv(EXCEPTION_TIME_ERROR_EXT+outfile,index=False,mode='a')
    else:
        df.to_csv(EXCEPTION_TIME_ERROR_EXT+outfile,index=False,mode='a',header=0)

# 解析gps数据
def parseGpsData(record,outfile):
    if len(record['gpsData']) > 0:
        for i in record['gpsData']:
            dic = {
                TITLE_SPORTID: [''],
                TITLE_ACTIVITY_TYPE: [''],
                TITLE_START_TIME: [''],
                TITLE_END_TIME: [''],
                TITLE_STEP_NUM: [''],
                TITLE_DIST: [''],
                TITLE_USED_TIME: [''],
                TITLE_CALORIES: [''],
                TITLE_HEIGHT: [''],
                TITLE_AVG_HR: [''],
                TITLE_AVG_SPEED: [''],
                TITLE_MAX_SPEED: [''],
                TITLE_MAX_FREQ: [''],
                TITLE_FINISHED_PERCENT: [''],
                TITLE_TIMEZONE: [''],
                TITLE_GPS: [''],
                TITLE_GPS_DATETIME:  [i['timeStamp']],
                TITLE_LATITUDE:      [i['latitude']],
                TITLE_LONGTITUDE:    [i['longitude']],
                TITLE_GPS_SPEED:     [i['speed']],
                TITLE_STATE:         [i['state']]
                }

            df = pd.DataFrame(dic)
            df.to_csv(outfile, index=False,header=False, mode='a')

# 解析运动详情数据
def parseSportData():
    print('sport data')

# 解析附加数据
def parseExtraData():
    print('extra data')

def parseOneSportRecordTmp(record,outfile):
    timeLocal = time.localtime(int(record['startTime']))
    # 转换成新的时间格式(2016-05-05 20:28:54)
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)
    timeLocal = time.localtime(int(record['endTime']))
    endTime = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)

    dic = {TITLE_SPORTID:[ record['sportId'] ],
           TITLE_ACTIVITY_TYPE: [ record['sportType'] ],
           TITLE_START_TIME: [ startTime ],
           TITLE_END_TIME:   [ endTime ],
           TITLE_STEP_NUM:   [ record['totalSteps'] ],
           TITLE_DIST:       [ record['totalDistance'] ],
           TITLE_USED_TIME:  [ record['totalTime'] ],
           TITLE_CALORIES:   [ record['totalCalories'] ],
           TITLE_HEIGHT:     [ record['totalHeight'] ],
           TITLE_AVG_HR:     [ record['avgHeartRate'] ],
           TITLE_AVG_SPEED:  [record['avgSpeed']],
           TITLE_MAX_SPEED:  [record['maxSpeed']],
           TITLE_MAX_FREQ:   [record['avgFrequency']],
           TITLE_FINISHED_PERCENT:  [record['achievePercent']],
           TITLE_TIMEZONE:      [record['timeZone']],
           TITLE_GPS:        ['gps数据'],
           TITLE_GPS_DATETIME:  [''],
           TITLE_LATITUDE:      [''],
           TITLE_LONGTITUDE:    [''],
           TITLE_GPS_SPEED:     [''],
           TITLE_STATE:         ['']
    }

    df = pd.DataFrame(dic)
    df.to_csv(outfile,index=False,mode='a')
    data = pd.read_csv(outfile)
    print(data.columns)
    parseGpsData(record,outfile)


# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseSportRecordTmp(inputfile,outfile):
    print ('需要转换的文件:'+inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    with open(inputfile,'r') as fd:
        jsonStr = json.load(fd)
        parseOneSportRecordTmp(jsonStr,outfile)
        print (jsonStr)
    print ('转换后文件保存：'+ outfile)