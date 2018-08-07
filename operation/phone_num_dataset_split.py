# -*- coding: utf-8 -*-
"""
@CREATETIME: 2018/8/7 14:09 
@AUTHOR: Chans
@VERSION: v1.0
"""


import pandas as pd
path = '/Users/Apple/Desktop/working/8 华院项目/花呗电话号码/tmp_shanxi_phone_num_1.csv'
data_pd = pd.read_csv(path,header=0,delimiter='\t',encoding='utf-8')
length = len(data_pd)
looper = length/500000 # 11
rest = (length-1) % 500000
for i in range(int(looper)+1) :
    path_out = '/Users/Apple/Desktop/working/8 华院项目/花呗电话号码/shanxi_dianxin/tmp_shanxi_dianxin_{}_{}.csv'.format(
        i * 500000 + 1, (i + 1) * 500000)
    if i < 10:
        tmp_array = data_pd[i * 500000 + 1:(i + 1) * 500000]
        tmp_array.to_csv(path_out, header=True, index=False)
    else:
        tmp_array = data_pd[i * 500000 + 1:length+1]
        tmp_array.to_csv(path_out, header=True, index=False)