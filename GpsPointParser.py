import pandas as pd
from ParseCommon import *
import time
import os
import struct
import simplekml
from collections import namedtuple

# 时间戳异常的数据的序列值
timeErrIndex = 0

# gps 打点数据格式
GPS_RECORD_ONE = '<?3xI2dfB3x'

# 解释一个 运动报告 数据，添加到excel文件中

def translate2kmlPath(latitude,longtitude,coordinates):
    coordinates.extend([(str(longtitude), str(latitude))])
    print('精度数据:'+ str(len(coordinates)))



def parseOneRecord(record,outfile,coordinates,index):
    hasData,timeStamp,latitude,longtitude,speed,state = struct.unpack(GPS_RECORD_ONE, record)

    timeLocal = time.localtime(int(timeStamp))
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

    dic = {TITLE_HAS_DATA: [ hasData ],
           TITLE_TIMESTAMP:[ timeStamp ],
           TITLE_DATETIME: [ dt ],
           TITLE_LATITUDE: [ latitude ],
           TITLE_LONGTITUDE: [longtitude],
           TITLE_GPS_SPEED: [ speed ],
           TITLE_STATE: [ state ]
            }

    translate2kmlPath(latitude,longtitude,coordinates)

    df = pd.DataFrame(dic)
    if index == 0:
        df.to_csv(outfile,index=False,mode='a')
    else:
        df.to_csv(outfile,index=False,mode='a',header=0)

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseGpsPoint(inputfile,outfile,kmoutfile):
    print ('需要转换的文件:'+inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    datetimeIndex = len(datetime) - 2

    print ('基础日期：'+datetime[datetimeIndex])
    index = 0
    currentTime = time.time()

    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile
    kmoutfile = path + kmoutfile

    isExist = os.path.exists(path)

    kml = simplekml.Kml(open=1)
    pnt = kml.newlinestring()
    pnt.name = '测试路径'
    pnt.description = '运动记录的测试轨迹'
    pnt.extrude = 1
    pnt.altitudemode = simplekml.AltitudeMode.relativetoground
    pnt.style.linestyle.width = 5
    pnt.style.linestyle.color = simplekml.Color.red
    coordinates = []

    if not isExist:
        os.makedirs(path)

    recordSize = struct.calcsize(GPS_RECORD_ONE)
    print('recordsize:' + str(recordSize))

    with open(inputfile,'rb') as fd:
        readbyte = fd.read(recordSize)

        while len(readbyte)>0 :
            parseOneRecord(readbyte, outfile,coordinates, index)
            readbyte = fd.read(recordSize)
            index = index + 1

    print('kml文件：' + kmoutfile)
    print('精度数据:' + str(len(coordinates)))
    pnt.coords = coordinates
    kml.save(kmoutfile)

    print ('转换后文件保存：'+ outfile)