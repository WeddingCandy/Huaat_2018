#coding=utf-8
import sys
import class_w2v
import preprocess
import numpy as np
import csv
import os

def input(trainname):
    """
    load file
    :param trainname:path
    :return: list
    """
    traindata = []
    with open(trainname, 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        count = 0
        for line in reader:
            try:
                traindata.append(line[0])
                count += 1
            except:
                print("error:", line, count)
                traindata.append(" ")
    return traindata

root_path = '/Users/Apple/datadata/labels/xxx'
if __name__ == '__main__':
    """
    使用方法：先训练wv的model，然后再生成wv的向量，最后可以使用2-fold验证效果
    主要目的：生成WV向量，提供给下一个步骤：特征融合。
    注意路径
    """
    print('---------w2v----------')
    # order = 'train w2v model'
    # order='getvec'
    order = 'test'

    print('order is', order)

    classob = class_w2v.w2v(300)

    if order == 'train w2v model': #训练WV的model
        totalname =root_path+os.sep+ 'writefile.csv' #纯文本文件路径
        classob.train_w2v(totalname)
        exit()
    elif order == 'getvec': #利用生成的model得到文档的WV的向量，使用求和平均法
        trainname = root_path + os.sep+'trainfile.csv'
        testname = root_path + os.sep+'testfile.csv'
        traindata = input(trainname)
        testdata = input(testname)
        res1 = classob.load_trainsform(traindata)
        res2 = classob.load_trainsform(testdata)
        print(res1.shape,res2.shape)
        np.save('wv300_win100.train.npy', res1)#保存生成的向量
        np.save('wv300_win100.test.npy', res2)
        exit()


    #以下为测试wv向量，即仅仅使用wv向量做这个比赛，目的在于寻找最好参数的WV向量
    print('载入所有的w2v向量中..')
    w2vtrain = np.load('wv300_win100.train.npy')
    w2vtest = np.load('wv300_win100.test.npy')

    #防止出现非法值
    if np.any((np.isnan(w2vtrain))):
        print('nan to num!')
        w2vtrain = np.nan_to_num(w2vtrain)

    if np.any((np.isnan(w2vtest))):
        print('nan to num!')
        w2vtest = np.nan_to_num(w2vtest)

    #载入label文件
    label_category = root_path + os.sep + 'label_train.csv'

    label_genderfile_path = '/Users/Apple/datadata/sougoudata_ori' + os.sep +'train_gender.csv'
    with open(label_category ,'r',encoding='utf-8') as f:
        labels_list = [x.strip() for x in f.readlines()]
        category_set =  set(labels_list)
    category_dict = {}
    for i, ele in enumerate(category_set):
        category_dict[ele] = i

    labels_list_transform = []
    for ele in labels_list:
        labels_list_transform.append(category_dict[ele])
    labels_list_transform = np.array(labels_list_transform)
    print(labels_list_transform[0:10])


    # genderdata = np.loadtxt(open(label_genderfile_path, 'r',encoding='utf-8')).astype(int)
    # print(genderdata.shape)


    print('预处理中..')
    preprocessob = preprocess.preprocess()
    gender_traindatas, genderlabel = preprocessob.removezero(w2vtrain, labels_list_transform)

    # ------------------------------------------------------

    if order == 'test': #使用2-fold进行验证
        res1 = classob.validation(gender_traindatas, genderlabel, kind='gender')
        print('avg is:', res1)
    else:
        print('error!')
        exit()
