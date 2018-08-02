# -*- coding: utf-8 -*-
"""
@CREATETIME: 16/05/2018 16:18
@AUTHOR: Chans
@VERSION: V1.0
"""

import pandas as pd
import re
import numpy as np
import os


"""                                            文件名   性别    年龄     人种  
0  1_Handshaking_Handshaking_1_158$$210_146_112_1...  0-男  2-中年  2-黄种人   
1  1_Handshaking_Handshaking_1_158$$464_240_52_94...  1-女  2-中年  2-黄种人   
2  1_Handshaking_Handshaking_1_158$$700_40_126_21...  0-男  3-老年  2-黄种人   
3          4_Dancing_Dancing_4_156$$529_51_65_93.jpg  0-男  2-中年   1-白人   
4  13_Interview_Interview_2_People_Visible_13_245...  1-女  2-中年   1-白人   
5  13_Interview_Interview_2_People_Visible_13_245...  0-男  2-中年   0-黑人   
6        38_Tennis_Tennis_38_323$$294_85_112_152.jpg  1-女  1-少年  2-黄种人   
"""

path_in = '/Users/Apple/datadata/human_face'
path_out = '/Users/Apple/datadata/human_face_output'

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


def main_process(excel_list,path_out,filename):
    for file in excel_list:
        ex = pd.read_excel(file,sheetname=r'标注结果',header=0)
        pic_name_list  =  ex.iloc[:, 0:1]
        pic_name_list = pic_name_list.values.tolist()


        # print(pic_name_list)
        print('----------------------')
        merged_name_list = []
        contents_dict = {}
        for i,pic_name in enumerate(pic_name_list):
            all_element = []
            pic_name = pic_name[0]
            name_element_list  = regexp_name_element_list(pic_name)
            print(name_element_list)
            name_main = regexp_name_main(pic_name)
            location = 0
            merged_name = ''
            for i , element_i in enumerate(name_element_list):
                if i <= 1 :
                    continue
                check_word = name_element_list[1]

                try:
                    check_index = name_element_list[2:].index(check_word)
                except Exception as e:
                    for i,ele2 in enumerate(name_element_list):
                        if i == 0:
                            continue
                        if i > 0 :
                            try:
                                ele2 = int(ele2)
                                if type(ele2) == type(0):
                                    location = i
                                    print(location)
                                    break
                            except:
                                pass



                if element_i == check_word:
                    location = i
                    print(element_i,check_word,i)
                    break
                    # print(location)

            if location == 2 :
                merged_name = name_element_list[0] + '--{}/{}.jpg'.format(name_element_list[1], name_main.group())
            elif location ==3 :
                merged_name = name_element_list[0] + '--{}_{}/{}.jpg'.format(name_element_list[1],name_element_list[2],
                                                                          name_main.group())
            elif location == 4:
                merged_name = name_element_list[0] + '--{}_{}_{}/{}.jpg'.format(name_element_list[1], name_element_list[2],
                                                                                name_element_list[3],name_main.group())
            merged_name_list.append(merged_name)
            # print(merged_name)
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
    path_in = '/Users/Apple/datadata/human_face' #in Mac
    path_out = '/Users/Apple/datadata/human_face_output'   #in Mac
    filename = 'test.txt'

    excel_list = Get_all_result_exels(path_in)
    main_process(excel_list,path_out,filename)

