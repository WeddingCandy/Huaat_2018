# -*- coding:utf-8 -*-

"""
@author:Jan
@file:人脸情绪识别.py
@time:2018/5/14 11:18
"""
from PIL import Image
from PIL import ImageDraw
import  re
import  os
# import cv2


path_in = '/Users/Apple/datadata/tmp2'
text_path = '/Users/Apple/datadata/wider_face_train_bbx_large.txt'
output_path = '/Users/Apple/datadata/temp'


with open(text_path, 'r', encoding='utf-8') as f:
    contents = [x.strip('\n') for x in f.readlines()]


def regexp_name(string):
    pattern = re.compile('([A-Za-z0-9_]+)\.jpg')
    strr = str(pattern.findall(string)[0])
    return strr

if __name__ == '__main__':
    folders = []



    for i,(root, dirs, files)  in enumerate(os.walk(path_in)):
        if i == 0:
            folders = dirs
            continue
        else:
            pass
        if i >0 :
            folder_name = folders[i-1]
            for file in files:
                if file != '.DS_Store':
                    match_name = folder_name + '/' +file
                    pic_path = root + os.sep + file

                    index = contents.index(match_name)
                    total_num_index = index + 1
                    total_num_amount =  int(contents[total_num_index])
                    print(total_num_amount)
                    for i in range(total_num_amount):
                        im = Image.open(pic_path)
                        # im.show()
                        boxx = contents[total_num_index + i + 1]
                        box_elements =  boxx.split()
                        box = []
                        for i , element in enumerate( box_elements):
                            if i <=1 :
                                box.append(int(element))
                            else:
                                box.append(int(box_elements[i-2])+int(element))
                        # print(type(box),box)
                        print(boxx,box)
                        draw = ImageDraw.Draw(im)
                        draw.rectangle(box, outline=(0, 255, 0))
                        pic_name = regexp_name(file)+'${}_{}_{}_{}.jpg'.format(box[0],box[1],box[2],box[3])
                        pic_save_path = output_path + os.sep + pic_name
                        im.save(pic_save_path)
                        # print(pic_save_path)

                        # im.show()
                else:
                    continue

    print('done')



