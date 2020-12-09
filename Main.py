########################################################
# 功能说明：
# 1 根据输入的文件类型，将输入数据翻译成excel文件。方便进行数据分析
#
########################################################

from DailyRecordParser import parseDailyRecord
from HrTmpParser import  *
from HrRestTmpParser import  *
from ParseCommon import *
from SportRecordTmpParser import parseSportRecordTmp
from DailyReportParser import *
from SleepParser import *
from SportReportParser import parseSportReport
from SportRecParser import parseSportRecord
from GpsPointParser import parseGpsPoint
from SpoIndexParser import parseSpoIndex
from SpoParser import parseSpo
from SpoTmpParser import parseSpoTmp
from sleepTmpParse import parseSleepTmp
from SportIndexParser import parseSportIndex
from stressTmpParser import parseStressTmp
from EventPointParser import parseEventPointData
from EventPointParser import parseEventPointIndex
from COMUtils import *
import sys
import time
import os
import uuid
from Gps2Kml import *

def help():
    print ('命令格式：python main.py param1  param2')
    print('param2 是需要解析的文件，完整路径')
    print('param1命令如下：')
    print('运动记录：'+ TRANSLATE_TYPE_SPORT_REC)

def _mainProcess():
    if len(sys.argv) >= 3:
        i = sys.argv[1]
        inputfile = sys.argv[2]
        print (inputfile)
    elif len(sys.argv) == 2:
        i = sys.argv[1]
        if i == '-h':
            help()
            return
    else:
        help()

    (path, filename) = os.path.split(inputfile)

    # 转换成localtime
    timeLocal = time.localtime(time.time())
    # 转换成新的时间格式(2016-05-05-20-28-54)
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

    for i in sys.argv:
        if i == TRANSLATE_TYPE_SPORT_REC:
            print ('运动记录数据解析：')
            parseSportRecord(inputfile, SPORT_REC_OUT_FILENAME_PRE + filename + '_' + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_SPORT_RPT:
            print ('运动报告数据解析：')
            parseSportReport(inputfile, SPORT_RPT_OUT_FILENAME_PRE + filename + '_' + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_SPORT_INDEX:
            print ('运动记录索引文件解析：')
            parseSportIndex(inputfile, SPORT_INDEX_OUT_FILENAME_PRE + filename + '_' + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_DA_REC:
            print ('每日活动记录解析：')
            parseDailyRecord(inputfile, DA_REC_OUT_FILENAME_PRE +  filename + '_' + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_DA_RPT:
            print ('每日活动报告解析：')
            parseDailyReport(inputfile, DA_RPT_OUT_FILENAME_PRE + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_SLEEP:
            print ('睡眠数据解析：')
            parseDailySleep(inputfile, SLEEP_OUT_FILENAME_PRE + filename + '_'+ dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_SPO:
            print ('血氧数据解析：')
            parseSpo(inputfile)
        elif i == TRANSLATE_TYPE_SPO_INDEX:
            print ('血氧索引文件解析：')
            parseSpoIndex(inputfile, SPO_INDEX_OUT_FILENAME_PRE + filename + '_' + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_SPO_TMP:
            print('血氧临时文件解析：')
            parseSpoTmp(inputfile, SPO_TMP_OUT_FILENAME_PRE+ filename + '_'+ dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_HR_TMP:
            print ('心率临时文件解析：')
            parseHrTmp(inputfile, HR_TMP_OUT_FILENAME_PRE + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_HR_REST_TMP:
            print ('静息心率临时文件解析：')
            parseHrRstTmp(inputfile, HR_RST_TMP_OUT_FILENAME_PRE + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_DA_TMP:
            print ('每日活动临时文件解析：')
            parseDaTmp(inputfile, DA_TMP_OUT_FILENAME_PRE + dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_STRESS_TMP:
            print ('压力临时文件解析：')
            parseStressTmp(inputfile, STRESS_TMP_OUT_FILENAME_PRE+ filename + '_'+ dt + OUT_FILE_EXT)
        elif i == TRANSLATE_TYPE_SPORT_REC_TMP:
            print ('运动记录临时json文件解析：')
            parseSportRecordTmp(inputfile, SPORT_REC_JSON_FILENAME_PRE + dt + OUT_FILE_EXT)
        elif i == GENERATE_UUID:
            print('生成UUID：')
            uid = str(uuid.uuid4())
            suid = ''.join(uid.split('-'))
            print('新生成的uid：'+ suid)
        elif i == TRANSLATE_TYPE_GPS2KML:
            print('将运动记录临时文件sportjson中的gps数据转换成kml文件')
            parseGpsDataToKml(inputfile)
        elif i == TRANSLATE_TYPE_GPS:
            print('将gps打点文件转换成excel文件和kml文件')
            parseGpsPoint(inputfile,SPORT_GPS_OUT_FILENAME_PRE + dt + OUT_FILE_EXT,SPORT_GPS_OUT_FILENAME_PRE \
                          + dt + KML_FILE_EXT)
        elif i == CONVERT_TO_C_ARRAY:
            print('将数据文件转换为c语言数组')
        elif i == TRANSLATE_EVENTPOINT_INDEX:
            print('解析埋点索引文件：')
            parseEventPointIndex(inputfile, EP_INDEX_FILENAME_PRE+ filename + '_'+ dt + OUT_FILE_EXT)
        elif i == TRANSLATE_EVENTPOINT_DATA:
            print('解析埋点数据文件')
            parseEventPointData(inputfile, EP_DATA_FILENAME_PRE+ filename + '_'+ dt + OUT_FILE_EXT)

if __name__ == '__main__':
    _mainProcess()