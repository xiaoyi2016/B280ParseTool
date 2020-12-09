import sys
import os
import time
import csv
import re

# 比较日常心率
CMP_HEARTRATE = '1'

# 比较血氧数据
CMP_SPO      = '2'

# 执行结果存储目录
TRANSLATED_FILE_DIR = 'result'

# 健康app同步的血氧数据文件
NORMAL_SPO_APP_FILE = 'appNormalResult.txt'
SLEEP_SPO_APP_FILE  = 'appResult.txt'


# 把心率数据中不需要的字串去掉 比如： 81:0 中的:0去掉，只保留心率数据
def processNotNeedStrHR(str):
    print('测试')
    return re.sub(r':[0-9],',',',str)

# 比较日常心率数据
# inputfile:  1天的日常打点数据解析后的csv文件
# inputfile2: 通过logcat抓取到的同步到健康app的数据文件。
# outfile：    比较的结果保存的文件
def cmpHeartRate(inputfile,inputfile2,outfile):
    (path, filename) = os.path.split(inputfile)
    matchResult = 1

    path = path + TRANSLATED_FILE_DIR
    outfile = path + outfile

    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    with open(inputfile,encoding='utf-8') as fd:
        reader = csv.reader(fd)
        header = next(reader)
        index = 0
        appText = ''

        with open(inputfile2,'r') as fd2:
            readbyte = fd2.readline()
            while len(readbyte) > 0:
              print(readbyte)
              startPos = int(readbyte.find("values="))
              if  startPos > 0:
                newText = readbyte[ startPos+7:len(readbyte)-1]
              else:
                newText = ''

              readbyte = fd2.readline()

              if len(newText) > 0:
                  print(newText)
                  newText2 = processNotNeedStrHR(newText)
                  appText = appText + newText2
                  print(appText)

            arrayAppText = appText.split(',')
            print(arrayAppText)
            for row in reader:
              if row[10] != arrayAppText[index]:
                  print('第'+str(index)+'行的数据不匹配')
                  matchResult = 0
              index = index + 1
            if matchResult == 1:
                print('原始数据和app获取的数据完全匹配')


# 比较血氧数据

# 比较睡眠血氧
def cmpSleepSPO(inputpath,Device,App,result):
    print('比较睡眠血氧')
    # 比较解析的数据和app同步到的数据
    appText = ''
    matchResult = 1

    with open(App, 'r') as fd2:
        readbyte = fd2.readline()
        while len(readbyte) > 0:
            print(readbyte)
            startPos = int(readbyte.find("values="))
            if startPos > 0:
                newText = readbyte[startPos + 7:len(readbyte) - 1]
            else:
                newText = ''

            readbyte = fd2.readline()

            if len(newText) > 0:
                print(newText)
                appText = appText + newText
                print(appText)

        arrayAppText = appText.split(',')
        print(arrayAppText)

    appOffset = 0
    for inputfile in Device:
        spotype = inputfile.split('_')
        # 判断是否读取的是普通血氧文件，如果是  跳过
        if spotype[0] == 'normal':
            continue
        fullinputfile = inputpath + '\\' + inputfile
        with open(fullinputfile, encoding='utf-8') as fd:
            reader = csv.reader(fd)
            header = next(reader)
            print('当前比较的文件是:'+inputfile)
            index = 0
            for row in reader:
                for index2 in range(appOffset,len(arrayAppText)-1):
                    if arrayAppText[index2] != '0':
                        appOffset = index2
                        print('appoffset=%d' %appOffset)
                        break
                    elif index2 == len(arrayAppText)-1:
                        appOffset = len(arrayAppText)

                if appOffset == len(arrayAppText):
                    break
                if row[2] != arrayAppText[appOffset]:
                    print('第' + str(index) + '行的数据不匹配')
                    print('手表数据 ' + row[2])
                    print('app端数据 ' + arrayAppText[appOffset])
                    matchResult = 0

                appOffset = appOffset + 1
                index = index + 1

    if matchResult == 1:
        print('原始数据和app获取的数据完全匹配')

# 比较普通血氧
# 把心率数据中不需要的字串去掉 比如： 81:0 中的:0去掉，只保留心率数据
def processNotNeedNormalSpo(str):
    return re.sub(r'->[0-9],',',',str)

def cmpNormalSPO(inputpath,Device,App,result):
    print('比较普通血氧')
    # 比较解析的数据和app同步到的数据
    appText = ''
    matchResult = 1

    with open(App, 'r') as fd2:
        readbyte = fd2.readline()
        while len(readbyte) > 0:
            print(readbyte)
            startPos = int(readbyte.find("values="))
            if startPos > 0:
                newText = readbyte[startPos + 7:len(readbyte)]
            else:
                newText = ''

            readbyte = fd2.readline()

            if len(newText) > 0:
                newText2 = processNotNeedNormalSpo(newText)
                appText = appText + newText2
                print(appText)

        arrayAppText = appText.split(',')
        print(arrayAppText)

    appOffset = 0
    for inputfile in Device:
        spotype = inputfile.split('_')
        # 如果不是普通血氧文件，则跳过
        if spotype[0] != 'normal':
            continue
        fullinputfile = inputpath + '\\' + inputfile
        with open(fullinputfile, encoding='utf-8') as fd:
            reader = csv.reader(fd)
            header = next(reader)
            print('当前比较的文件是:'+inputfile)
            index = 0
            for row in reader:
                for index2 in range(appOffset,len(arrayAppText)-1):
                    if arrayAppText[index2] != '0':
                        appOffset = index2
                        break
                    elif index2 == len(arrayAppText)-1:
                        appOffset = len(arrayAppText)

                if appOffset == len(arrayAppText):
                    break
                if row[2] != arrayAppText[appOffset]:
                    print('第' + str(index) + '行的数据不匹配')
                    print('手表数据 ' + row[2])
                    print('app端数据 ' + arrayAppText[appOffset])
                    matchResult = 0

                appOffset = appOffset + 1
                index = index + 1

    if matchResult == 1:
        print('原始数据和app获取的数据完全匹配')

# inputPath:  手表拉取的血氧数据解析后的文件路径
#             健康app抓取的logcat中数据请按照下面命名，并且放在和血氧数据解析后的同一路径下
#             普通血氧数据文件命名为：  appNormalResult.txt
#             睡眠血氧文件命名为：     appResult.txt
# outfile:   比较的结果保存的文件
def cmpSPO(inputPath,outfile):
    filelist = os.listdir(inputPath)

    # 对文件按照时间戳进行重新排序,并把睡眠和普通血氧分开
    newFileArray = []
    timeArray    = []

    for filename in  filelist:
      datetime = filename.split('_')

      # 判断是否是app的结果文件，如果是 跳过
      if len(datetime) < 3:
          print(filename + '  skip')
          continue

      newtime = datetime[len(datetime)-3]

      if len(timeArray) == 0:
          timeArray.append(newtime)
          newFileArray.append(filename)
      else:
          if newtime > timeArray[len(timeArray)-1]:
             timeArray.append(newtime)
             newFileArray.append(filename)
          else:
              for tempIndex in range(0,len(timeArray)-1):
                  if newtime < timeArray[tempIndex]:
                      timeArray.insert(tempIndex,newtime)
                      newFileArray.insert(tempIndex,filename)
                      break

    sleepDataFile = inputPath + '\\' + SLEEP_SPO_APP_FILE
    # cmpSleepSPO(inputPath,newFileArray,sleepDataFile,outfile)
    normalDataFile = inputPath + '\\' + NORMAL_SPO_APP_FILE
    cmpNormalSPO(inputPath,newFileArray,normalDataFile,outfile)


def help():
    print('参数错误')

def _mainProcess():
    if len(sys.argv) >= 4:
        i = sys.argv[1]
        inputfile = sys.argv[2]
        inputfile2 = sys.argv[3]
        print (inputfile)
        print(inputfile2)
    else:
        help()

    (path, filename) = os.path.split(inputfile)

    # 转换成localtime
    timeLocal = time.localtime(time.time())
    # 转换成新的时间格式(2016-05-05-20-28-54)
    dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

    for i in sys.argv:
        if i == CMP_HEARTRATE:
            print ('比较日常心率数据：')
            cmpHeartRate(inputfile, inputfile2,filename + '_' + dt + '_cmp.result')
        elif i == CMP_SPO:
            print('比较血氧数据：')
            cmpSPO(inputfile, filename + '_' + dt + '_cmp.result')


if __name__ == '__main__':
    _mainProcess()