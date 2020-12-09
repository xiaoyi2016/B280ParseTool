import pandas as pd
from ParseCommon import *
import time
import os
import struct
from collections import namedtuple


def parseOneSportRecord(record,dataFormat,nameList,outfile,datetime,index,currentTime):
    sportReport = namedtuple('sportReport',nameList)
    data = sportReport._make(struct.unpack(dataFormat,record))

    timeLocal = time.localtime(int(data.timeStamp ))
    endtimelocal = time.localtime(int(data.timestampEnd ))

    # 转换成新的时间格式
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    dtend = time.strftime("%Y-%m-%d-%H-%M-%S", endtimelocal)



# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseSportReport(inputfile,outfile):
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

    with open(inputfile,'rb') as fd:
        # 第一部分
        recordSize = struct.calcsize(SPORT_RECORD_PART_ONE)
        readbyte = fd.read(recordSize)
        nameList = ['version', 'sportType', 'timeStamp', 'timeTick', 'timestampEnd', 'timeZone', 'autoflag']
        sportReport = namedtuple('sportReport', nameList)
        dataOne = sportReport._make(struct.unpack(SPORT_RECORD_PART_ONE, readbyte))
        timeLocal = time.localtime(int(dataOne.timeStamp))
        endtimelocal = time.localtime(int(dataOne.timestampEnd))
        # 转换成新的时间格式
        dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
        dtend = time.strftime("%Y-%m-%d-%H-%M-%S", endtimelocal)

        # 第二部分
        recordSize = struct.calcsize(SPORT_RECORD_PART_TWO)
        perKm = fd.read(recordSize)

        # 第三部分
        recordSize = struct.calcsize(SPORT_RECORD_PART_THREE)
        readbyte = fd.read(recordSize)
        nameListThree = ['perKmLen', 'finishPercent', 'sportSubType', 'stanimalLevel', 'maxHeartRate', 'gameCounts', 'gameStess']
        sportReportThree = namedtuple('sportReportThree', nameListThree)
        dataThree = sportReportThree._make(struct.unpack(SPORT_RECORD_PART_THREE, readbyte))

       # 第四部分
        recordSize = struct.calcsize(SPORT_RECORD_PART_FOUR)
        readbyte = fd.read(recordSize)
        print('读到的字节数 '+str(len(readbyte)))
        nameListFour = ['hasData', 'sTime', 'timeTotal', 'distance', 'calories', 'heartrate', \
                         'heartrateMax','heartrateAvg','heartrateZone','heartrateZone1','heartrateZone2', \
                         'heartrateZone3','heartrateZone4','heartrateZone5','stamina','pace','paceAvg', \
                         'paceBest','altitude','heightTotal','stepNum','stepFreqAvg','VO2Max','trainEffect', \
                         'recoveryTime','speed','speedAvg','spo2','spo2Avg','activityType']
        sportReportFour = namedtuple('sportReportFour', nameListFour)
        dataFour = sportReportFour._make(struct.unpack(SPORT_RECORD_PART_FOUR, readbyte))

        dic = {
            TITLE_VERSION: [dataOne.version],
            TITLE_SPORT_TYPE: [getSportName(dataOne.sportType)],
            TITLE_TIMESTAMP: [dataOne.timeStamp],
            TITLE_DATETIME: [dt],
            TITLE_TIMESTAMP_END: [dataOne.timestampEnd],
            TITILE_END_DATETIME: [dtend],
            TITLE_TIMEZONE: [dataOne.timeZone],
            TITLE_AUTOFLAG: [dataOne.autoflag],
            TITLE_KMLEN: [ dataThree.perKmLen ],
            TITLE_FINISHED_PERCENT: [ dataThree.finishPercent ],
            TITLE_STAMINA_LEVEL: [ dataThree.stanimalLevel ],
            TITLE_MAX_HR: [ dataThree.maxHeartRate ],
            TITLE_GAME_COUNTS: [ dataThree.gameCounts ],
            TITLE_GAME_STRESS: [ dataThree.gameStess ]


        }

        df = pd.DataFrame(dic)
        df.to_csv(outfile, index=False, mode='a')
    print ('转换后文件保存：'+ outfile)