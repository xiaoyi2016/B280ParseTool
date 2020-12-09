import os
import sys

def help():
    print('参数错误，请检查参数个数')

def mainProcess():
    if len(sys.argv) >= 3:
        i = sys.argv[1]
        inputfile = sys.argv[2]
        print (inputfile)
    elif len(sys.argv) == 2:
        i = sys.argv[1]
    else:
        help()

    os.system('adb shell pm')

if __name__ == '__main__':
    mainProcess()