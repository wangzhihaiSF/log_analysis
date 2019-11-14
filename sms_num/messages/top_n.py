import json
import os
import csv
import argparse
from sms_num.messages.find_str import getSubStr_offset
# 日志存放的路劲，若放到服务器需要绝对路劲
g_cur_file_path = os.path.abspath(os.path.dirname(__file__))
parser = argparse.ArgumentParser(description='top_n')
parser.add_argument("-log", "--log", help="logfile full name", default="-1")
parser.add_argument("-out", "--out", help="output full name", default="-1")
parser.add_argument("-input", "--input", help="input full file name", default="-1")
parser.add_argument("-top", "--top", help="top n", default=100, type=int)
args = parser.parse_args()


class HandleLog:
    def __init__(self):
        self.sms_dict = {}
        self.sOut = ''
        self.nTop = 100
        self.save_file_name = self.create_file_name()

    def get_result(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as fp:
                for line in fp:
                    self.process_data(line)
        except OSError:
            print("出错啦! 文件貌似不存在。。。")

    def process_data(self, line):
        next_begin = 0
        while 1:
            num, offset = getSubStr_offset(line, "androidId", "smsNumber", 3, "\",", endoffset=0, beginOffset=next_begin)
            if offset < 0:
                break
            if num not in self.sms_dict:
                self.sms_dict[num] = 1
            else:
                self.sms_dict[num] += 1
            next_begin = offset

    def write_data_all(self, sFile):
        self.sOut = sFile
        cols = ["短信号", "商户名称", "所属行业", "数量"]
        self.write_data(cols)
        # 降序排序
        sorted_sms_dict = sorted(self.sms_dict.items(), key=lambda x: x[1], reverse=True)
        n = 0  # 统计短信量为1的接入号的数量
        json_dict = self.load_json()
        for i in sorted_sms_dict[0:self.nTop]:
            if i[1] > 1:  # 过滤短信数量小于1的机构号码
                if i[0] in json_dict:  # 和json 文件进行自动的机构和号码匹配
                    new_list = [i[0]] + json_dict[i[0]] + [i[1]]
                    self.write_data(new_list)
                else:
                    new_list = [i[0]] + [" "] + [" "] + [i[1]]
                    self.write_data(new_list)
            else:
                n += 1

    def write_data(self, data):
        file_name = self.save_file_name
        with open(file_name, "a", encoding="utf-8-sig", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(data)

    def create_file_name(self):
        file_name = self.sOut + "messages" + args.input[:-4] + ".csv"
        return file_name

    def load_json(self):
        with open("sms_num.json", 'r', encoding="utf-8") as f:
            json_dict = json.load(f)
        return json_dict


def my_main():
    if 1:
        print('in test mode')
        args.input = input("请输入文件名字")
        args.log = g_cur_file_path + '/' + args.input
        args.out = g_cur_file_path
    if args.out == '-1' or args.log == '-1':
        print('check cmdline ', args)
        return
    if args.top == '-1':
        print('check cmdline ', args)
        return
    hand_log = HandleLog()
    hand_log.nTop = args.top
    hand_log.get_result(args.log)
    hand_log.write_data_all(args.out)


if __name__ == "__main__":
    my_main()
