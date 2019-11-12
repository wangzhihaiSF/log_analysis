import csv
import os
g_cur_file_path = os.path.abspath(os.path.dirname(__file__))


class WeekMessages():
    def __init__(self):
        pass

    def read_csv(self, file_name):
        with open(file_name, "r", encoding="utf-8") as fp:
            csv_file = csv.reader(fp)
            return csv_file


if __name__ == "__main__":
    week_messages = WeekMessages()
    csv_file = week_messages.read_csv('../20191112.csv')
    for i in csv_file:
        print(i)

