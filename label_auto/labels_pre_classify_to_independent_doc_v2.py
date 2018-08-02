# -*- coding:UTF-8 -*
import pandas as pd
import re
import numpy as np
from jieba import posseg as pg
import jieba
import jieba.analyse
import os
"""
用来将新扒下来的标签切词分类。
其中有：
1.过滤词，过滤网页专业术语词；
2.文档只包含一级大类和HEAD信息
"""

# jieba.enable_parallel()

def modify_output(s):
    pattern1 = re.compile('[ \[\]\'《》\<\>‘’“”\"\(\)]+')
    line1 = pattern1.sub(' ',s)
    line1.replace("\[",' ').replace("\'",' ').replace("\]",' ')
    pattern2 = re.compile('\s{2,}')
    line2 = pattern2.sub(' ',line1)
    line2.strip()
    return line2

def stop_words(stop_words_list):
    stopwords_list = [line.strip() for line in open(stop_words_list, 'r', encoding='utf-8').readlines()]
    l1 = sorted(set(stopwords_list), key=stopwords_list.index)
    print(l1)
    return l1


def line_to_words(s,stopwords_list):
    strxx = " "
    try:
        line = pg.cut(s)
        allowPOS = ['n', 'v', 'a', 'ns', 'ad', 't', 's', 'vn', 'nr', 'nt']
        for word in line:
            if word.flag in allowPOS:
                if len(word.word) > 1 and word.word not in stopwords_list:
                    strxx += word.word + " "
                else :
                    continue
        return strxx
    except Exception as e:
        print(e)
        return 'NOTHING'

def load_docs(aim_excel,stop_words_list,label_list):
    stopwords_list = stop_words(stop_words_list)
    data = pd.read_excel(aim_excel, sheet_name='Sheet2', header=0, encoding='utf-8')
    data_length = len(data)
    with open(label_list, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        label_list_dic = {}
        for line in lines:
            line = line.split(' ')
            label_list_dic[line[0]] = line[1].strip()
    print(label_list_dic)

    return  data,label_list_dic,data_length ,stopwords_list

def main_process(aim_excel,stop_words_list,label_list):
    data, label_list_dic, data_length,stopwords_list = load_docs(aim_excel,stop_words_list,label_list)
    COUNT = 0
    for i in range(data_length):
        try:
            if data.iloc[i:i+1,0:1].values != data.iloc[i+1:i+2,0:1].values:
                COUNT = 0
            file_class = label_list_dic[(data.iloc[i:i+1,0:1].values).tolist()[0][0]]
            contents = str((data.iloc[i:i+1,1:2].values).tolist()[0][0])
            contents_modified = modify_output(contents)
            contents_fenci = line_to_words(contents_modified,stopwords_list)

            if contents != 'nan' and contents !='NOTHING':
                COUNT += 1
                file_name =path_output+os.sep+file_class+'_'+str(COUNT)+'.txt'
                with open(file_name,'w',encoding='utf-8') as f:
                    f.write(contents_fenci)

        except Exception as e:
            file_class = (data.iloc[-2:-1, 0:1].values).tolist()[0][0]
            contents = str((data.iloc[-2:-1, 1:2].values).tolist()[0][0])
            contents = modify_output(contents)
            if contents != 'nan' or contents != 'NOTHING':
                file_name = path_output + os.sep + file_class + '_' + str(999) + '.txt'
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(contents)
    print('done')



path_output = r'C:\Users\thinkpad\Desktop\crawlers\labels\level1\output'
aim_excel = r"C:\Users\thinkpad\Desktop\crawlers\labels\level1\labels_original_trainset.xlsx"
stop_words_list =r'C:\Users\thinkpad\Desktop\crawlers\labels\level1\filter_voc.txt'
label_list =  r'C:\Users\thinkpad\Desktop\crawlers\labels\level1_lablelist_with_original_name.txt'

if not  os.path.exists(path_output):
    os.mkdir(path_output)



do = main_process(aim_excel,stop_words_list,label_list)



