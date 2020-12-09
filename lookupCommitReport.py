#coding=utf-8

import os
import sys
import time

OUTPUT_FILE_NAME    = 'B281 UI人员提交记录_'
GERRTI_CMD_PATH = "\"ssh -p 29418 wanjie1@partnerrd.longcheer.com gerrit query"
GERRI_LOOKUP_CMD    = " status:merged before:"
GERRIT_LOOUP_CMD2   = " after:"
GERRIT_LOOUP_CMD3   = " | grep -ic \'"
GERRIT_LOOUP_END    = "\' \" "
GIT_CMD_PATH = " \"C:\\Program Files\\Git\\bin\\bash.exe\" -c "

TITLE_NAME      =   '姓名'
TITLE_COMMIT    =   '提交的记录数量'


def lookupZhName(english):
    if english == "username: gongliyong":
        return "龚利勇"
    elif english == "username: wangdonghai":
        return "王东海"
    elif english == "username: liushuigen1":
        return "刘水根"
    elif english == "username: jiangguoping1":
        return "蒋国平"
    elif english == "username: guoyao":
        return "郭侥"
    elif english == "username: zhoutao":
        return "周涛"
    elif english == "username: quanzhonghu":
        return "全忠虎"
    elif english == "username: zouzongze":
        return "邹宗泽"
    elif english == "username: linjie":
        return "林杰"
    elif english == "username: liuzhicai":
        return "刘志财"


# 查询一个人的提交记录
def loopupOne(name,startTime,endTime,outfile):
    execCmd = GIT_CMD_PATH + GERRTI_CMD_PATH + GERRI_LOOKUP_CMD + endTime + GERRIT_LOOUP_CMD2 +startTime + GERRIT_LOOUP_CMD3 + name + GERRIT_LOOUP_END
    print('执行的命令：'+execCmd)
    returnValue = os.popen(execCmd).readlines()
    print (lookupZhName(name),file=outfile)
    print(' ',file=outfile)
    for i in returnValue:
       print(i,file=outfile)



def help():
    print ('命令格式：lookupCommitReport.exe param1  param2 param3')
    print('param1 查询的开始日期 格式参考： 2020-08-19')
    print('param2 查询的结束日期 格式参考： 2020-08-20')
    print('param3 要查询人员的配置清单')

def mainProcess(argv):
    try:
        if len(argv) >= 4:
            startTime = argv[1]
            endTime = argv[2]
            configFile = argv[3]
        else:
            help()
            return

        # 转换成localtime
        timeLocal = time.localtime(time.time())
        # 转换成新的时间格式(2016-05-05-20-28-54)
        dt = time.strftime("%Y-%m-%d-%H-%M-%S", timeLocal)

        outfile = '.\\'+ OUTPUT_FILE_NAME + dt+ '.log'
        doc = open(outfile, 'a')
        print('B281 深圳UI人员,从' + startTime + '到' + endTime + '代码提交统计：', file=doc)
        with open(configFile, 'r') as fd:
            while True:
                line = fd.readline().replace('\n','').replace('\r','')
                if line:
                    loopupOne(line,startTime,endTime,doc)
                else:
                    break

        doc.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print('开始执行')
    mainProcess(sys.argv)