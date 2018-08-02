#! /usr/bin/env python
# coding=utf-8
import time,  sched
import datetime
import os
import schedule
import time
import re
import threading
import multiprocessing

def monitor_text():

    def log_output():
        path = r'C:\huabei_logs'
        cur_date = int(time.time())
        filename = '{}.txt'.format(cur_date)
        print("Now output txt" + str(cur_date))
        with open(path + '\\' + filename, 'w', encoding='utf-8') as f:
            f.write(str(cur_date))

    schedule.every(10).seconds.do(log_output)

    while True:
        schedule.run_pending()
        time.sleep(1)


def check():
    def difference():
        path = r'C:\huabei_logs'
        path_list = os.walk(path)

        for root, dirs, files in path_list:
            latest_log = files[-1]
            pattern = re.compile('\.txt')
            log_time = int(pattern.sub('',latest_log ))

        cur_date_unix = int(time.time())
        print(cur_date_unix -  log_time)

    schedule.every(15).seconds.do(difference)
    while True:
        schedule.run_pending()
        time.sleep(1)

    # return log_time

if __name__ == '__main__':

    print('go')



    p1 = multiprocessing.Process(target=monitor_text)
    p2 = multiprocessing.Process(target=check)
    p1.start()
    p2.start()
    p1.join()
    p2.join()




