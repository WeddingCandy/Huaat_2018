# -*- coding: utf-8 -*-
"""
@CREATETIME: 2018/8/7 14:09 
@AUTHOR: Chans
@VERSION: v1.0
"""


import pandas as pd
path = '/Users/Apple/Desktop/working/8 华院项目/花呗电话号码/phone_number_cmcc_tb2.csv'
data_pd = pd.read_csv(path,header=0,delimiter='\t',encoding='utf-8')
length = len(data_pd)
looper = int(length/800000) # 11
rest = (length-1) % 800000
for i in range(int(looper)+1) :
    print(i)
    path_out = '/Users/Apple/Desktop/working/8 华院项目/花呗电话号码/shanxi_yidong/tmp_shanxi_yidong_{}_{}_20180817.csv'.format(
        i * 800000 + 1, (i + 1) * 800000)
    if i < looper:
        tmp_array = data_pd[i * 800000 + 1:(i + 1) * 800000]
        tmp_array.to_csv(path_out, header=True, index=False)
    else:
        tmp_array = data_pd[i * 800000 + 1:i * 800000 + rest ]
        tmp_array.to_csv(path_out, header=True, index=False)