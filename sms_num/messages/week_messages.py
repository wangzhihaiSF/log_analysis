import csv
from datetime import datetime
from sms_num.messages import top_n
import os
g_cur_file_path = os.path.abspath(os.path.dirname(__file__))


class WeekMessages(object):
    def __init__(self):
        self.file_names = self.get_file_name()
        self.data_list = []

    def read_csv(self, file_name):
        sub_list = []
        try:
            with open(file_name, "r", encoding="utf-8") as fp:
                read = csv.reader(fp)
                for line in read:
                    sub_list.append(line)
            self.data_list.append(sub_list)
        except OSError:
            print("%s 文件不存在，将自动生成。" % file_name)
            top_n.my_main()
            print("文件生成成功")
            self.read_csv(file_name)

    def rea_all_csv(self):
        for i in self.file_names:
            self.read_csv(i)

    # 需要整合的文件名字，前 n 天的短信日报表
    def get_file_name(self, n=2):
        names = []
        today_int = int(self.get_today_str())
        for day in range(today_int - n, today_int):
            file_name = "messages" + str(day) + ".csv"
            names.append(file_name)
        return names

    def process_two_file(self, file1_data_list, file2_data_list):
        not_in = []
        for i in file1_data_list[1:]:  # 去掉第一行的列名
            for j in file2_data_list[1:]:
                if j[0] == i[0]:
                    i[3] = str(int(j[3]) + int(i[3]))
                    continue
                else:
                    not_in.append(j)
        file1_data_list += not_in

    def process_all_file(self):
        self.get_file_name()
        for file_name in self.file_names:
            self.read_csv(file_name)
        n = 1
        while n < len(self.data_list):
            self.process_two_file(self.data_list[0], self.data_list[n])
            n += 1

    def get_today_str(self):
        today = datetime.now()
        return today.strftime("%Y%m%d")

    def write_result(self):
        result_name = "weekmessages" + self.get_today_str() + ".csv"
        sorted_list = sorted(self.data_list[0], key=(lambda x: x[3]), reverse=True)
        with open(result_name, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for item in sorted_list[0]:
                writer.writerow(item)


def my_main():
    week_messages = WeekMessages()
    week_messages.rea_all_csv()
    week_messages.process_all_file()
    week_messages.write_result()


if __name__ == "__main__":
    my_main()








