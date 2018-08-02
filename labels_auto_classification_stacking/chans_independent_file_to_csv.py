# -*- coding: utf-8 -*-
"""
@CREATETIME: 22/05/2018 14:55 
@AUTHOR: Chans
@VERSION: V1.0
"""

import os,re

# input_path ='/Users/Apple/datadata/labels/output_test'
output_path ='/Users/Apple/datadata/labels/xxx'

def classification_extract(str):
    pattern = re.compile('_[0-9]+|.txt')
    str = pattern.sub('',str)
    return str

def main_process(input_path,input_file1,input_file2 ):
    name_list = []
    for root,dirs,files in os.walk(input_path):
        for file in files:
            if file != '.DS_Store':
                name = root + os.sep + file
                name_list.append([name, classification_extract(file)])
            else:
                continue

    whole_test_set = []
    whole_label_set = []

    for i,f_c in enumerate(name_list):
        with open(f_c[0], 'r', encoding='utf-8') as f:
            contents = f.readline()
        if i == 0:
            classification1 = f_c[1]
            contents_list = []
            contents_list.append(contents)
            whole_test_set.append(contents)
            whole_label_set.append(classification1)
            continue
        elif i > 0 and len(contents.split()) >3:
            classification2 = f_c[1]
            if classification2 == classification1 :
                contents_list.append(contents)
                whole_test_set.append(contents)
                whole_label_set.append(classification2)
            else:
                # print(contents_list)
                classification1 = classification2
                # file_name = output_path+os.sep+classification1+'_test'+'.csv'
                # with open(file_name,'w',encoding='utf-8') as ff:
                #     for x in contents_list :
                #         if len(x.split()) > 3 :
                #             ff.write(x +'\n')
                contents_list = []
                contents_list.append(contents)
                whole_test_set.append(contents)
                whole_label_set.append(classification1)

    file_name1 = output_path + os.sep + 'content_' + input_file1
    file_name2 = output_path + os.sep + 'label_' + input_file2
    with open(file_name1,'w',encoding='utf-8') as fff:
        for x in whole_test_set:
            fff.write(x+'\n')
    with open(file_name2,'w',encoding='utf-8') as fff:
        for x in whole_label_set:
            fff.write(x+'\n')
    print('done')



main_process('/Users/Apple/datadata/labels/output_tmp','train.csv','train.csv')
main_process('/Users/Apple/datadata/labels/output_test','test.csv','test.csv')




