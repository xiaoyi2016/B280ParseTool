
# 把二进制数据文件 转换为 c 语言数组

READ_SIZE  = 16

def  convert2CArray(dataFile,outFile):
    fdOut = open(outFile,'w+')
    fdOut.write('static const char dataArray = { ')
    with open(dataFile, 'rb') as fd:
        readbyte = fd.read(READ_SIZE)

        while len(readbyte) > 0:
            for i in range(0, 15):
                print("0x%x" % readbyte[i])

            readbyte = fd.read(READ_SIZE)

    fdOut.write('};')