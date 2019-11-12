def getSubStr_offset(sLine, sPreFlag, sBeginFlag, sBeginOffset, sEndFlag, endoffset=0, beginOffset=0):
    preLogid = 0
    if sPreFlag != '':
        preLogid = sLine.find(sPreFlag, beginOffset)
        if preLogid < 0:
            return '', -1
    ret_begin = preLogid
    if sBeginFlag != "":
        ret_begin = sLine.find(sBeginFlag, preLogid)
        if ret_begin < 0:
            return '', -2

    ret_begin += sBeginOffset + len(sBeginFlag)

    ret_end = len(sLine) - 1
    if sEndFlag != '':
        ret_end = sLine.find(sEndFlag, ret_begin)
    ret_end = ret_end - endoffset
    if ret_end < 0:
        return '', -3
    sId = sLine[ret_begin:ret_end]
    return sId, ret_end


sFile = ""
if __name__ == '__main__':
    with open(sFile, encoding="utf-8") as f:
        while 1:
            line = f.readline()
            if line == "":
                break
            num, re = getSubStr_offset(line, "", "smsSign", 3, "\",")
            print(num, " : ", re)
            pass
