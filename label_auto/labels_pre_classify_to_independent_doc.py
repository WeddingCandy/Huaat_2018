# -*- coding:UTF-8 -*
import pandas as pd
import re
import numpy as np
from jieba import posseg as pg
import jieba
import os
"""
用来将一级大类单独分出文档，切词，尾号自增。
"""

# jieba.enable_parallel()

def modify_output(s):
    pattern1 = re.compile('[ \[\]\'‘’“”\"\(\)]+')
    line1 = pattern1.sub(' ',s)
    line1.replace("\[",' ').replace("\'",' ').replace("\]",' ')
    pattern2 = re.compile('\s{2,}')
    line2 = pattern2.sub(' ',line1)
    line2.strip()
    return line2

def line_to_words(s):
    strxx = " "
    try:
        line = pg.cut(s)
        allowPOS = ['n', 'v', 'a', 'ns', 'ad', 't', 's', 'vn', 'nr', 'nt']
        for word in line:
            if word.flag in allowPOS:
                strxx += word.word + " "
        return strxx
    except Exception as e:
        print(e)
        return 'NOTHING'



path_main = r'C:\Users\thinkpad\Desktop\crawlers\labels\output'
path_in = r"C:\Users\thinkpad\Desktop\crawlers\labels\标签爬虫结果2.xlsx"
# path_level1_test_in = r"C:\Users\thinkpad\Desktop\crawlers\labels\labels_testset_1.xlsx"
# path_in = r"C:\Users\thinkpad\Desktop\crawlers\labels\标签爬虫结果test.xlsx"
# path_out = r"C:\Users\thinkpad\Desktop\crawlers\labels\level2_result.xlsx"
# path_level1_test_out = r"C:\Users\thinkpad\Desktop\crawlers\labels\labels_testset_result_1.xlsx"
# data = pd.read_csv(path, sep=',', encoding='utf-8',engine='python',header=0)
label_list =  r'C:\Users\thinkpad\Desktop\crawlers\labels\level1_lablelist_with_original_name.txt'
data = pd.read_excel(path_in,sheet_name='results',header=0,encoding='utf-8')
data.rename(columns={'行业一级大类':'class1','行业二级大类':'class2'}, inplace = True)
data_length= len(data)

data_type = "level1"

with open(label_list,'r',encoding='utf-8') as f:
    lines = f.readlines()
    label_list_dic = {}
    for line in lines:
        line = line.split(' ')
        label_list_dic[line[0]] = line[1].strip()

print(label_list_dic)




if data_type == "level1":
    COUNT = 0
    for i in range(data_length):
        try:
            if data.iloc[i:i+1,0:1].values != data.iloc[i+1:i+2,0:1].values:
                COUNT = 0

            file_class = label_list_dic[(data.iloc[i:i+1,0:1].values).tolist()[0][0]]
            contents = str((data.iloc[i:i+1,3:4].values).tolist()[0][0])
            contents_modified = modify_output(contents)
            contents_fenci = line_to_words(contents_modified)

            if contents != 'nan' and contents !='NOTHING':
                COUNT += 1
                file_name =path_main+os.sep+file_class+'_'+str(COUNT)+'.txt'
                with open(file_name,'w',encoding='utf-8') as f:
                    f.write(contents_fenci)

        except Exception as e:
            file_class = (data.iloc[-2:-1, 0:1].values).tolist()[0][0]
            contents = str((data.iloc[-2:-1, 3:4].values).tolist()[0][0])
            contents = modify_output(contents)
            if contents != 'nan' or contents != 'NOTHING':
                file_name = path_main + os.sep + file_class + '_' + str(999) + '.txt'
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(contents)

    print('done')






