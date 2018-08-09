# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
import re
import os

def read_match_info(file):
    pd_match_info = pd.read_excel(file,encoding = 'utf-8',header=0)
    columns_match_info = ['销售代表编码', '销售代表名称', '营业员手机号', '支付宝账号认证人', '营业员绑定支付宝', 'UID']
    pd_match_info_aim = pd_match_info[columns_match_info]
    return pd_match_info_aim

def read_detail(file):
    pd_detail = pd.read_excel(file,encoding = 'utf-8',header=0)
    return  pd_detail

def search_new_input_file(file_path):
    import os
    import re
    import datetime
    date = (datetime.date.today() + datetime.timedelta(days = -1)).strftime('%m%d')

    all_files = []
    aim_file =''
    for root, dirs, files in os.walk(file_path):
        all_files = files
    print(all_files,date)
    pattern1 = '[\w-]+{}\.xlsx'.format(date)
    reg_exp = re.compile(pattern1)
    for file in all_files:
        if len(reg_exp.findall(file))>0 :
            aim_file =reg_exp.findall(file)[0]
    print(aim_file)
    return aim_file

 date = datetime.datetime.now().strftime('%Y%m%d')