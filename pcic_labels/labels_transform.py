# -*- coding: utf-8 -*-
"""
@CREATETIME: 03/07/2018 13:35 
@AUTHOR: Chans
@VERSION: V1.0
"""

import pandas as pd
import numpy as np
import collections


file_input_path = r'/Users/Apple/Desktop/working/8 华院项目/太平洋保险/太平洋-游族数据/华院分析数据测试标签.xlsx'
dict_input_path = r'/Users/Apple/Desktop/working/8 华院项目/太平洋保险/太平洋-游族数据/MobData标签映射华院标签.xlsx'
file_output_path = r'/Users/Apple/Desktop/working/8 华院项目/太平洋保险/太平洋-游族数据/output3.xlsx'


dict_pd = pd.read_excel(dict_input_path ,header=0)
dict_np = np.array(dict_pd)
dictt ={}
for  ele in dict_np :
    x = ele.tolist()
    dictt[x[0]] = x[-2:]


data = pd.read_excel(file_input_path,sheetname=r'应用偏好',header=0)
print(data[0:10])

data_length = len(data)
x_length =2925

save = [] #[ [imei,['一级','二级'],['一级','二级'] ] ]

for i in range(data_length) :
    x = data.iloc[i]
    tmp_list = []
    for j,t in enumerate(x):
        if j == 0:
            tmp_list.append(t)
            continue
        if t == 1:
            type_index = (x.index)[j]
            tmp_list.append(dictt[type_index])
    tmp_list2 = []
    for ii in tmp_list :

        if ii not in tmp_list2:
            tmp_list2.append(ii)
    save.append(tmp_list2)

data_output = pd.DataFrame(columns=['imei','level1','level2'])


save_transform = []
for t, ele in enumerate(save) :
    # dict_save = {}
    dict_save =collections.defaultdict(list)
    for i,el in enumerate(ele):
        if i == 0:
            imei = el
        else:
            dict_save_keys = list(dict_save.keys())
            dict_save[el[0]].append(el[1])
            dict_end = dict(dict_save)
    for j in dict_end :
        row = {'imei':imei,'level1':j,'level2':dict_end[j]}
        data_output = data_output.append(row,ignore_index=True)




data_output.to_excel(file_output_path,sheet_name='Output',index=False,encoding='utf-8')



    # x_list = list(x)
    # print(x_list)