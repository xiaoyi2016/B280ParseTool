import serial
import time
import threading
import serial.tools.list_ports
from ParseCommon import *

# 串口输出保存到文件
UART_OUTPUT_FILE_PATH   =  "D:\\04-download\\04-log\\"

# 串口交互命令输出特别的分割符
UART_CMD_OUTPUT_BEGIN   = '>22ee82e77e4f4f6f82feeb0a97bf43ab>'
UART_CMD_OUTPUT_END     = '<22ee82e77e4f4f6f82feeb0a97bf43ab<'

# 串口配置
COM_PORT_NUM  = 'COM24'

COM_PORT_SPEED = 115200
# 超时设置 5 秒
COM_TIMEOUT    = 5

# 把文件缓存刷新进入文件的门限
UPDATE_FILE_COUNT   = 20

# 发送命令给串口和等待返回的超时时间。 单位 秒
WAIT_COM_RETURN_TIMER    = 10

# 读取的数据
DATA=""
# 是否读取结束
NOEND = True

# 结束函数返回。 超时或者收到返回的数据
ENDALL = False

# 发送命令的回调函数参数内容,错误码和消息内容。 如果正常返回数据，则消息体就是返回的内容
errorCode = ''
errorMsg = ''

updateCount = UPDATE_FILE_COUNT

# 循环读取串口数据
def readData(ser,doc):
    global  DATA,NOEND,updateCount,ENDALL,errorCode,errorMsg

    while(NOEND):
        if ser.in_waiting:
            DATA = ser.read(ser.in_waiting).decode('gbk')
            timeLocal = time.localtime(time.time())
            # 转换成新的时间格式(2016-05-05-20-28-54)
            dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

            print("\n"+dt+">>  ",DATA,"\n>>",end="",file=doc)
            updateCount = updateCount - 1
            if updateCount == 0:
                updateCount = UPDATE_FILE_COUNT
                doc.flush()
            doc.close()
            ENDALL = True

# 打开串口
def openSerial(portNum,bps,timeoutTimer):
    ret = False
    try:
        ser = serial.Serial(portNum,bps,timeout=timeoutTimer)

        timeLocal = time.localtime(time.time())
        # 转换成新的时间格式(2016-05-05-20-28-54)
        dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

        logfile = UART_OUTPUT_FILE_PATH + dt + "_uart.log"

        doc = open(logfile,'a')

        if(ser.is_open):
            ret = True
            th = threading.Thread(target=readData, args=(ser,doc))
            th.daemon = 1
            th.start()
    except Exception as e:
        print ("error:",e)
    return ser,ret

# 关闭串口
def closeSerial(ser):
    global  NOEND
    NOEND = False
    ser.close()

# 写数据
def writeToSerial(ser,text):
    res = ser.write(text.encode("gbk"))
    return res

# 读数据
def readFromSerial():
    global  DATA
    data = DATA
    # 清空当次读取
    DATA = ""
    return data


# 通过串口发送命令并等待返回，如果超过时间就自动返回超时错误
def SendDataByCom(content,cb):
    global errorCode,errorMsg,ENDALL
    timeCount = 0

    print ('串口程序启动')
    portlist = list(serial.tools.list_ports.comports())
    if len(portlist) == 0:
        print ('无可用串口')
        errorCode = COM_ERROR_CODE_TIMEOUT
        errorMsg = '串口通信超时'
        cb(errorCode,errorMsg)
    else:
        for i in range(0,len(portlist)):
            print ('可用的串口如下：',portlist[i])

    try:
        ser,ret = openSerial(COM_PORT_NUM,COM_PORT_SPEED,COM_TIMEOUT)

        while ENDALL:
            writeToSerial(ser,content)
            time.sleep(1)
            timeCount = timeCount + 1

            if timeCount >= WAIT_COM_RETURN_TIMER:
                ENDALL = True

        closeSerial(ser)
        cb(errorCode,errorMsg)
    except Exception as e:
        print ("串口操作异常：",e)
        return