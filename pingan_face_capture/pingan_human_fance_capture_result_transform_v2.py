# -*- coding: utf-8 -*-
"""
@CREATETIME: 23/05/2018 11:39 
@AUTHOR: Chans
@VERSION: V2.0
"""


import pandas as pd
import re
import numpy as np
import os

def Get_all_result_exels(path):
    excel_list = []
    for root,dirs,files in os.walk(path):
        for file in files:
            if file != '.DS_Store':
                excel_list.append(root+os.sep+file)
            else:
                pass
    return excel_list

def Write_output_to_txt(path,filename,dict):
    with open(path + os.sep + filename, 'w', encoding='utf-8') as f:
        for key in dict.keys():
            amount = len(dict[key])
            f.write(key+'\n')
            f.write(str(amount)+'\n')
            # print(amount)
            for i in range(amount):
                f.write(dict[key][i]+'\n')
    print('done')


def regexp_name_element_list(list):
    pattern1 = re.compile('_|\$|\.jpg')
    out_put = (pattern1.sub(' ', list)).split()
    return out_put


def regexp_name_main(list):
    pattern2 = re.compile('([\w]+)')
    out_put = pattern2.match(list)
    return out_put

def regexp_all_element(list):
    pattern3 = re.compile('\d|-1')
    path_out = pattern3.match(list)
    path_out = path_out.group()
    return path_out


def Get_pic_name_list(file):
    ex = pd.read_excel(file, sheetname=r'标注结果', header=0)
    pic_name_list = ex.iloc[:, 0:1]
    pic_name_list = pic_name_list.values.tolist()
    return pic_name_list

def Load_category_name_dict(file):
    category_dict = {}
    with open(file,'r',encoding='utf-8') as f:
        contents  = f.readlines()
        for x in contents:
            x = x.split()
            category_dict[x[0]] = x[1]
    return category_dict


def main_process(excel_list,path_out,filename,mapping_file):
    for file in excel_list:
        ex = pd.read_excel(file,sheetname=r'标注结果',header=0)
        pic_name_list  =  ex.iloc[:, 0:1]
        pic_name_list = pic_name_list.values.tolist()


        # print(pic_name_list)
        print('----------------------')
        merged_name_list = []
        contents_dict = {}
        category_dict = Load_category_name_dict(mapping_file)
        for i,pic_name in enumerate(pic_name_list):
            all_element = []
            pic_name = pic_name[0]
            name_element_list  = regexp_name_element_list(pic_name)
            # print(name_element_list)
            name_main = regexp_name_main(pic_name)
            location = 0
            merged_name = ''
            category_name = category_dict[name_element_list[0]]
            merged_name = category_name+'/{}.jpg'.format(name_main.group())
            # print(merged_name)
            merged_name_list.append(merged_name)

            coordinate = [ int(x) for x in name_element_list[-4:] ]
            coordinate_origin = []
            for i2, element in enumerate(coordinate):
                if i2 <= 1:
                    coordinate_origin.append(str(element))
                else:
                    coordinate_origin.append(str(-int(coordinate[i2 - 2]) + int(element)))

            coordinate_origin_str = ' '.join(coordinate_origin)

            all_element.append(coordinate_origin_str)
            col_num = ex.columns.size
            for i3 in range(1,col_num):
                tmp =  ex.iloc[i:i+1,i3:i3+1].values[0][0]
                if type(tmp) == type(0):
                    tmp = str(tmp)

                tmp2 = regexp_all_element(tmp)
                # print(type(tmp2))
                all_element.append(tmp2)


            all_element_dispose = '\t'.join(all_element)

            if merged_name not in contents_dict.keys():
                contents_dict[merged_name] = [all_element_dispose]
            else :
                contents_dict[merged_name].append(all_element_dispose)

        Write_output_to_txt(path_out,filename,contents_dict)



if __name__ == '__main__':
    path_in = '/Users/Apple/datadata/pingan_human_face/human_face' #in Mac
    path_out = '/Users/Apple/datadata/pingan_human_face/human_face_output'   #in Mac
    mapping_file = '/Users/Apple/datadata/pingan_human_face/human_face_mapping.txt'
    filename = '20180531-Train.txt'

    excel_list = Get_all_result_exels(path_in)
    main_process(excel_list,path_out,filename,mapping_file)

