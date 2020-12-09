import pandas as pd
from ParseCommon import *
import os
import time

# 解释一个每日活动报告数据，添加到excel文件中
#


# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseDailyReport(inputfile,outfile):
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
        record = fd.read()

    # 创建结构体对象
    bytebufT = byte_buffer_t()
    byte_buffer_create(bytebufT, record, len(record))

    timeLocal = time.localtime(int(datetime[datetimeIndex]))
    # 转换成新的时间格式(2016-05-05 20:28:54)
    basetime = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)
    stepnumber = byte_buffer_get_int(bytebufT, 0)
    exerciseTime = byte_buffer_get_short(bytebufT,0)

    calories = byte_buffer_get_short(bytebufT,0)
    activeStatus = byte_buffer_get_uint(bytebufT, 0)

    distance = byte_buffer_get_int(bytebufT, 0)
    floor = byte_buffer_get_short(bytebufT, 0)
    stress = byte_buffer_get_byte(bytebufT, 0)
    stressMin = byte_buffer_get_byte(bytebufT, 0)
    stressMax = byte_buffer_get_byte(bytebufT, 0)
    activityType = byte_buffer_get_byte(bytebufT, 255)

    dic = {TITLE_BASE_DT: [ basetime ],
           TITLE_STEP_NUM: [stepnumber],
           TITLE_DATETIME: [exerciseTime],
           TITLE_CALORIES: [calories],
           TITLE_ACTIVITY_STATUS: [activeStatus],
           TITLE_DIST: [distance],
           TITLE_FLOOR: [floor],
           TITLE_STRESS: [stress],
           TITLE_STRESS_MIN: [stressMin],
           TITLE_STRESS_MAX: [stressMax],
           TITLE_ACTIVITY_TYPE: [activityType],
   }

    df = pd.DataFrame(dic)


    df.to_csv(outfile, index=None, mode='a')

    print (outfile+" 转换结束")