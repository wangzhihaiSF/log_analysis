import os
g_cur_file_path = os.path.abspath(os.path.dirname(__file__))
import csv
from datetime import datetime
from sms_num.find_str import getSubStr_offset
import argparse
parser = argparse.ArgumentParser(description='top_n')
parser.add_argument("-log", "--log", help="logfile full name",default="-1")
parser.add_argument("-out", "--out", help="output full name",default="-1")
parser.add_argument("-top", "--top", help="top n",default=100,type=int)
args = parser.parse_args()


class HandleLog:
    def __init__(self):
        self.sms_dict = {}
        self.sOut = ''
        self.nTop = 100
    def get_result(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as fp:
                for line in fp:
                    self.process_data(line)
        except OSError:
            print("出错啦! 文件貌似不存在。。。")
    def process_data(self, line):
        nextBegin = 0
        while 1:
            num,offset = getSubStr_offset(line,"androidId", "smsNumber", 3, "\",",endoffset=0,beginOffset=nextBegin)
            if offset< 0:
                break
            if  num not in self.sms_dict:
                self.sms_dict[num] = 1
            else:
                self.sms_dict[num] += 1
            nextBegin = offset

    def write_data_all(self,sFile):
        self.sOut = sFile
        # 降序排序
        sorted_sms_dict = sorted(self.sms_dict.items(), key=lambda x: x[1], reverse=True)
        n = 0  # 统计短信量为1的接入号的数量
        for i in sorted_sms_dict:
            if i[1] > 1:  # 过滤短信数量小于1的机构号码
                self.write_data(i)
            else:
                n += 1
    def write_data(self, data):
        today = datetime.now()
        file_name = self.sOut + today.strftime("%Y%m%d") + ".csv"
        with open(file_name, "a", encoding="utf-8", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(data)

def myMain():
    if 1:
        print('in test mode')
        args.log = g_cur_file_path +'/real_log.log'
        args.out = g_cur_file_path +'/myout'
    if args.out == '-1' or args.log == '-1':
        print('check cmdline ',args)
        return
    if args.top == '-1':
        print('check cmdline ',args)
        return
    hand_log = HandleLog()
    hand_log.nTop = args.top
    hand_log.get_result(args.log)
    hand_log.write_data_all(args.out)
if __name__ == "__main__":
    myMain()

