# -*- coding: utf-8 -*-
"""
@CREATETIME: 17/07/2018 17:28
@AUTHOR: Chans
@VERSION:
"""
import pandas as pd
import numpy as np
import time

gender_map={'男':1,'女':0,'未知':2}
age_map={'18岁以下':0,'18-24岁':1,'25-34岁':2,'35-44岁':3,'45岁以上':4}
edu_map={'高中及以下':0,'专科':1,'本科及以上':2}
child_map={'无未成年子女':0,'0-3岁（婴幼儿）':1,'4-6岁（学龄前）':2,'7-12岁（小学生）':3,'13-17岁（初、高中生）':4,'其他':5}
income_map={'小于3K':0,'3-6K':1,'6-10K':2,'10-20K':3,'20K以上':4,'50k以上':5}
marriage_map={'未婚':0,'已婚':1,'未知':2}
house_map={'无房':0,'有房':1,'未知':2}
car_map={'无车':0,'有车':1,'未知':2}


gender_map1={v: k for k, v in gender_map.items()}
age_map1={v: k for k, v in age_map.items()}
edu_map1={v: k for k, v in edu_map.items()}
child_map1={v: k for k, v in child_map.items()}
income_map1={v: k for k, v in income_map.items()}
marriage_map1={v:k for k,v in marriage_map.items()}
house_map1={v:k for k,v in house_map.items()}
car_map1={v:k for k,v in car_map.items()}

dict_list = [gender_map1,age_map1,edu_map1,child_map1,income_map1,marriage_map1,house_map1,car_map1]


file_path = '/Users/Apple/Desktop/working/8 华院项目/sony电视报告需求/tmp_ana_cyw_sony_ec_check_aimed_user_base_info.txt'
with open(file_path,'r',encoding='utf-8') as f:
    data = [content.split() for content in   f.readlines()]
columns = ['leader_id','gender_map','age_map','edu_map','child_map',
           'income_map','marriage_map','house_map','car_map']
data_pd = pd.DataFrame(data=data,columns=columns)

pd_length = len(data_pd)

# shape = np.zeros(data_pd.shape )
# data_pd_out = pd.DataFrame(data = shape,columns=columns)
col_length = len(data_pd.columns)

print('start')
time_count1 = time.time()
for i in range(col_length):
    if i == 0:
        continue
    data_pd[columns[i]] = data_pd[columns[i]].astype(int)

count1 = 0
count2 = 0
count3 = 0
for i in range(len(data_pd)) : #到最后一行
    if i % 1000 == 0 :
        print(i)
    # data_pd.head(n=5).iloc[0:5,1:]
    if list((data_pd.iloc[i:i+1,2:3] == 0).values[0])[0] and list((data_pd.iloc[i:i+1,6:7] == 1 ).values[0])[0]   :
        data_pd.iloc[i:i+1, 6:7] = 0
        count1 += 1
    if list((data_pd.iloc[i:i+1,2:3] == 0).values[0])[0] and list((data_pd.iloc[i:i+1, 4:5]!= 0).values[0])[0]:
        count2 += 1
        data_pd.iloc[i:i + 1, 4:5] = 0
    if list((data_pd.iloc[i:i+1,2:3] == 1).values[0])[0] and list((data_pd.iloc[i:i+1,4:5] >= 3).values[0])[0] :
        data_pd.iloc[i:i+1, 4:5] = 1
        count3 += 1

time_count2 = time.time()
print(time_count2-time_count1)
print('{},{};{},{};{},{}'.format(count1,count1/pd_length,count2,count2/pd_length,count3,count3/pd_length))
print(data_pd.head())
for i in range(col_length):
    if i == 0:
        continue
    data_pd[columns[i]] = data_pd[columns[i]].map(dict_list[i-1])

    # for t in range(col_length):
    #     if t == 0:
    #         continue
    #     data_pd_out.iloc[i:i+1,t:t+1] = dict_list[t-1][int(list(data_pd.iloc[i:i+1,t:t+1].values[0])[0])]

file_path_out = '/Users/Apple/Desktop/working/8 华院项目/sony电视报告需求/tmp_ana_cyw_sony_ec_check_aimed_user_base_info.xlsx'
data_pd.to_excel(file_path_out,index=False,header=True,encoding='utf-8')
time_count3 = time.time()
print(time_count3-time_count2)


