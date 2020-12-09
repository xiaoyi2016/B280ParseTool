import pandas as pd
from ParseCommon import *
import time
import os

#  每日活动记录的单个数据结构的大小
DAILY_RECORD_SIZE = 19

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

def parseOneDailyRecord(record,outfile,datetime,index,currentTime):
    print ('parse one daily record start:')
    # 创建结构体对象
    bytebufT = byte_buffer_t()
    byte_buffer_create(bytebufT,record,len(record))

    # 相对文件记录起始地址的时间戳偏移值
    timestamp = byte_buffer_get_short(bytebufT,0)
    realTimeStamp = int(datetime) + timestamp*60
    # 转换成localtime
    timeLocal = time.localtime(realTimeStamp)
    basetimeLocal = time.localtime(int(datetime))
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    dtBase = time.strftime("%Y-%m-%d-%H-%M-%S", basetimeLocal)

    distance_inc = byte_buffer_get_short(bytebufT,0)
    step_number_inc = byte_buffer_get_short(bytebufT,0)

    calories_inc = byte_buffer_get_byte(bytebufT,0)
    height_inc = byte_buffer_get_byte(bytebufT,0)

    heartrate = byte_buffer_get_byte(bytebufT, 0)
    heartrateMin = byte_buffer_get_byte(bytebufT, 0)
    heartrateMax = byte_buffer_get_byte(bytebufT, 0)
    heartrateStatus = byte_buffer_get_byte(bytebufT, 0)
    heartrateRest = byte_buffer_get_byte(bytebufT, 0)

    stress = byte_buffer_get_byte(bytebufT, 0)
    stressStatus = byte_buffer_get_byte(bytebufT, 0)

    spo2 = byte_buffer_get_byte(bytebufT, 0)
    spo2Status = byte_buffer_get_byte(bytebufT, 0)

    hasWear = byte_buffer_get_bits_byte(bytebufT,3,3,0)
    hasSport = byte_buffer_get_bits_byte(bytebufT,2,2,0)
    hasExercise = byte_buffer_get_bits_byte(bytebufT,1,1,0)
    hasSleep = byte_buffer_get_bits_byte(bytebufT,0,0,0)

    byte_buffer_move_byte(bytebufT)

    activity_type = byte_buffer_get_byte(bytebufT, 0)

    print('bytebuffer offset:'+str(bytebufT.offset))
    print ('时间戳：'+ str(timestamp))
    dic = {TITLE_TIMESTAMP:[ realTimeStamp ],
           TITLE_DATETIME: [ dt ],
           TITLE_BASE_DT: [ dtBase ],
           TITLE_INC_TIMESTAMP: [ timestamp ],
           TITLE_WEAR: [hasWear],
           TITLE_CALORIES: [ calories_inc],
           TITLE_DIST:[ distance_inc ],
           TITLE_HAS_SPORT:[ hasSport ],
           TITLE_HEIGHT:[ height_inc ],
           TITLE_STEP_NUM:[ step_number_inc ],
           TITLE_HR:[ heartrate ],
           TITLE_HR_MIN:[ heartrateMin ],
           TITLE_HR_MAX:[ heartrateMax ],
           TITLE_HR_REST:[ heartrateRest ],
           TITLE_HAS_SLEEP:[ hasSleep ],
           TITLE_SPO2:[ spo2 ],
           TITLE_STRESS:[ stress ],
           TITLE_SPO2_QUALITY:[ spo2Status ],
           TITLE_STRESS_QUALITY: [ stressStatus ],
           TITLE_HR_QUALITY: [ heartrateStatus ],
           TITLE_HAS_EXERCISE:[ hasExercise ],
           TITLE_ACTIVITY_TYPE:[ activity_type ],
           }

# 保留成excel文件
#   append_to_excel(df,dic,outfile,index)
# 保留成csv文件
    if realTimeStamp > currentTime:
        print ("时间戳异常")
       # saveTimeErrorData(outfile,index,dic,timeErrIndex)

    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a')
    else:
        df.to_csv(outfile,index=False,mode='a',header=0)

    print ('parse one daily record end')

# 保存成excel文件 start
def create_excel(outfile):
    df = pd.DataFrame()
    df.to_excel(outfile,index=False)

def append_to_excel(df,contentList,outfile,index):
    ds = pd.DataFrame(contentList)
    df = df.append(ds,ignore_index=True)
    if index == 0:
        df.to_excel(outfile,index=False)
    else:
        df.to_excel(outfile,index=False,header=False)
# 保存成excel文件 end

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseDailyRecord(inputfile,outfile):
    print ('需要转换的文件:'+inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    datetimeIndex = len(datetime)-2
    print ('基础日期：'+datetime[datetimeIndex])
    index = 0
    currentTime = time.time()
    timeErrIndex = 0
    # create_excel(outfile)
    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    with open(inputfile,'rb') as fd:
        readbyte = fd.read(DAILY_RECORD_SIZE)
        while len(readbyte)>0 :
            # df = pd.read_excel(outfile, header=None)
            parseOneDailyRecord(readbyte,outfile,datetime[datetimeIndex],index,currentTime)
            readbyte = fd.read(DAILY_RECORD_SIZE)
            index = index + 1
    print ('转换后文件保存：'+ outfile)