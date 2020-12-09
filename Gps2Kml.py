import json

import pandas as pd
from ParseCommon import *
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import time
import os
import simplekml

# 把运动记录文件中的gps数据提取出来，转换为kml文件 导入google地图中查看位置信息

# 解析gps数据
def parseGpsData(record,outfile):
    if len(record['gpsData']) > 0:
        for oneData in record['gpsData']:
            timeLocal = time.localtime(int(oneData['timeStamp']))
            # 转换成新的时间格式(2016-05-05 20:28:54)
            startTime = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)

            dic = {
                TITLE_GPS_DATETIME:  [startTime],
                TITLE_LATITUDE:      [oneData['latitude']],
                TITLE_LONGTITUDE:    [oneData['longitude']],
                TITLE_GPS_SPEED:     [oneData['speed']],
                TITLE_STATE:         [oneData['state']]
                }

            df = pd.DataFrame(dic)
            df.to_csv(outfile, index=False,header=False, mode='a')

    else:
        print('没有gps数据')

def parseOneSportRecordTmp(record,outfile):
    timeLocal = time.localtime(int(record['startTime']))
    # 转换成新的时间格式(2016-05-05 20:28:54)
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)
    timeLocal = time.localtime(int(record['endTime']))
    endTime = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)

    dic = {TITLE_GPS_DATETIME:  [],
           TITLE_LATITUDE:      [],
           TITLE_LONGTITUDE:    [],
           TITLE_GPS_SPEED:     [],
           TITLE_STATE:         []
    }

    df = pd.DataFrame(dic)
    df.to_csv(outfile,index=False,mode='a')
    data = pd.read_csv(outfile)
    parseGpsData(record,outfile)

def translate2kml(record,outfile):
    kml = simplekml.Kml(open=1)
    pnt = kml.newpoint()
    pnt.coords = [(record['gpsData'][0]['longitude'], record['gpsData'][0]['latitude'])]

    # 剩余的点追加到folder
    for i in range(1,len(record['gpsData'])):
        pnt = kml.newpoint()
        pnt.coords = [(record['gpsData'][i]['longitude'], record['gpsData'][i]['latitude'])]

    print('kml文件：' + outfile )
    kml.save(outfile)

def translate2kmlPath(record,outfile):
    kml = simplekml.Kml(open=1)
    pnt = kml.newlinestring()
    pnt.name = '测试路径'
    pnt.description = '运动记录的测试轨迹'
    pnt.extrude = 1
    pnt.altitudemode = simplekml.AltitudeMode.relativetoground
    pnt.style.linestyle.width = 5
    pnt.style.linestyle.color = simplekml.Color.red
    coordinates = []

    for i in range(0, len(record['gpsData'])):
        if 0 == record['gpsData'][i]['longitude']:
            if 0 == record['gpsData'][i]['latitude']:
                continue
        coordinates = coordinates + [(record['gpsData'][i]['longitude'], record['gpsData'][i]['latitude'])]
        # pnt.coords.append([(record['gpsData'][i]['longitude'], record['gpsData'][i]['latitude'])])

    pnt.coords = coordinates
    print('kml文件：' + outfile)
    kml.save(outfile)

def testkml(outfile):
    kml = simplekml.Kml(open=1)
    single_point = kml.newpoint(name="The World", coords=[(0.0, 0.0)])
    cities = [
        ('Aberdeen, Scotland', '5:00 p.m.', 57.15, -2.15),
        ('Adelaide, Australia', '2:30 a.m.', -34.916667, 138.6),
        ('Algiers, Algeria', '6:00 p.m.', 36.833333, 3),
        # ...many, many more cities, and then...
        ('Zurich, Switzerland', '6:00 p.m.', 47.35, 8.516667)
    ]
    for city, time, lat, lon in cities:
        pnt = kml.newpoint()
        pnt.name = city
        pnt.description = "Time corresponding to 12:00 noon, Eastern Standard Time: {0}".format(time)
        pnt.coords = [(lon, lat)]
        kml.save(outfile)

# inputfile: 需要转换的文件 完整路径
# outfile:   转换后的文件 完整路径
def parseGpsDataToKml(inputfile):
    print ('需要转换的文件:'+inputfile)
    (path, filename) = os.path.split(inputfile)
    datetime = filename.split('_')
    path = path + TRANSLATED_FILE_DIR
    # 转换成localtime
    timeLocal = time.localtime(time.time())
    # 转换成新的时间格式(2016-05-05-20-28-54)
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)
    outfile = filename + '_gps_' + dt + '.csv'
    kmOutFile = filename + '_' + dt + '.kml'
    outfile = path + outfile
    kmOutFile = path + kmOutFile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    with open(inputfile,'r') as fd:
        jsonStr = json.load(fd)
        parseOneSportRecordTmp(jsonStr,outfile)
        # translate2kml(jsonStr,kmOutFile)
        translate2kmlPath(jsonStr,kmOutFile)
        # testkml(kmOutFile)
        # print (jsonStr)
    print ('转换后文件保存：'+ outfile)