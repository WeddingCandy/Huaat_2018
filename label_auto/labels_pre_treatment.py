# -*- coding:UTF-8 -*
import pandas as pd
import re
"""
用来将训练集的一级、二级大类合并

"""


##用于清楚无用的字符等
def modify_output(s):
    pattern1 = re.compile('[ \[\]\',，、。\"\(\)]+')
    line1 = pattern1.sub(' ',s)
    line1.replace("\[",' ').replace("\'",' ').replace("\]",' ')
    pattern2 = re.compile('\s{2,}')
    line2 = pattern2.sub(' ',line1)
    line2.strip()
    return line2

path_in = r"C:\Users\thinkpad\Desktop\crawlers\labels\标签爬虫结果.xlsx"
path_level1_test_in = r"C:\Users\thinkpad\Desktop\crawlers\labels\labels_testset_1.xlsx"
# path_in = r"C:\Users\thinkpad\Desktop\爬虫\labels\标签爬虫结果test.xlsx"
path_out = r"C:\Users\thinkpad\Desktop\crawlers\labels\level2_result.xlsx"
path_level1_test_out = r"C:\Users\thinkpad\Desktop\crawlers\labels\labels_testset_result_1.xlsx"
# data = pd.read_csv(path, sep=',', encoding='utf-8',engine='python',header=0)
data = pd.read_excel(path_level1_test_in,sheet_name='Sheet1',header=0,encoding='utf-8')
data.rename(columns={'行业一级大类':'class1','行业二级大类':'class2'}, inplace = True)
data_length= len(data)

data_type = "level1" #一级大类、二级大类整合选项level1、level2
if data_type == "level1":
    data['level1_output'] = 'NULL'
    for i in range(data_length):
        xx= []
        yy= []
        try:
            if data.iloc[i:i+1,0:1].values ==data.iloc[i+1:i+2,0:1].values:
                data.iloc[i:i+1,-1:] = '0'
            if data.iloc[i:i+1,0:1].values !=data.iloc[i+1:i+2,0:1].values:
                xx = (data.iloc[i:i + 1, -2:-1].values).tolist()
                yy = modify_output(str(xx))
                data.iloc[i:i+1, -1:] = yy
        except Exception as e:
            # print("Exception: {}".format(e))
            xx = (data.iloc[1:i + 1, -2:-1].values).tolist()
            yy = modify_output(str(xx))
            data.iloc[i:,-1:] = yy

    odata = data[data['level1_output'] !='0']
    odata =odata.reset_index()
    odata_length = len(odata)
    for i in range(odata_length):
        print(i)
        x = (odata.loc[i:i,'level1_output'].values).tolist()
        y = modify_output(x[0])
        odata.loc[i:i, 'level1_output'] = y

    odata.to_excel(path_level1_test_out, sheet_name='level1')
    print('done')

if data_type == "level2":
    data['level2_output'] = 'NULL'
    for i in range(data_length):
        xx= []
        yy= []
        try:
            if data.iloc[i:i+1,0:1].values ==data.iloc[i+1:i+2,0:1].values & data.iloc[i:i+1,1:2].values ==data.iloc[i+1:i+2,1:2].values:
                data.iloc[i:i+1,-1:] = '0'
                print(data.iloc[i:i+1,-1:])
            if data.iloc[i:i+1,0:1].values !=data.iloc[i+1:i+2,0:1].values & data.iloc[i:i+1,1:2].values !=data.iloc[i+1:i+2,1:2].values:
                xx = (data.iloc[i:i + 1, -2:-1].values).tolist()
                yy = modify_output(str(xx))
                data.iloc[i:i+1, -1:] = yy
        except Exception as e:
            # print("Exception: {}".format(e))
            xx = (data.iloc[1:i + 1, -2:-1].values).tolist()
            yy = modify_output(str(xx))
            data.iloc[i:,-1:] = yy

    odata = data[data['level2_output'] !='0']
    odata =odata.reset_index()
    odata_length = len(odata)
    for i in range(odata_length):
        print(i)
        x = (odata.loc[i:i,'level2_output'].values).tolist()
        y = modify_output(x[0])
        odata.loc[i:i, 'level2_output'] = y
    odata.to_excel(path_out, sheet_name='level2')
    print('done')





