# coding=utf-8
import classify
import preprocess
import pandas as pd
import numpy as np
import csv
import codecs
import multiprocessing
import time , os
# import sys


def input(trainname):
    """
    load the text file
    :param trainname: path of the input file
    :return:list
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
                traindata.append("1")
    return traindata
def output(filename, ID, age, gender, education):
    """
    generate the submit file
    :param filename: path of the submit file
    :param ID: user ID
    :param age:predicted age
    :param gender:predicted gender
    :param education:predicted education
    :return:submit file
    """
    print(ID.shape, age.shape, gender.shape, education.shape)
    with codecs.open(filename, 'w', encoding='gb18030') as f:
        count=0
        for i in range(len(ID)):
            # if count>=1000:
            #     break
            f.write(str(ID[i]) + ' ' + str(age[i]) + ' ' + str(gender[i]) + ' ' + str(education[i]) + '\n')
            count+=1
if __name__ == '__main__':

    """
    the main function
    注意路径
    """
    # root_path = '/Users/Apple/datadata/sougoudata_ori'
    root_path = '/Users/Apple/datadata/labels/xxx'
    start=time.time()
    # order='predict' #execute predict function
    order='test' #execute 2-fold validation function
    print('order is ', order)
    print('----------start----------')

    #loading
    trainname = root_path +os.sep+ 'content_train.csv'
    testname =root_path +os.sep+ 'content_test.csv'
    traindata = input(trainname)
    testdata = input(testname)
    label_genderfile_path =root_path + os.sep + 'label_test.csv'
    with open(label_genderfile_path ,'r',encoding='utf-8') as f:
        labels_list = [x.strip() for x in f.readlines()]
        category_set =  set(labels_list)
    category_dict = {}
    for i, ele in enumerate(category_set):
        category_dict[ele] = i

    labels_list_transform = []
    for ele in labels_list:
        labels_list_transform.append(category_dict[ele])
    labels_list_transform = np.array(labels_list_transform)

    # ---------------------------------
    print('预处理开始')
    pre_time_start = time.time()
    preprocessob = preprocess.preprocess()

    #remove label missed samples
    gender_traindatas, genderlabel = preprocessob.removezero(traindata, labels_list_transform)
    print(gender_traindatas.shape,gender_traindatas.shape[0])



    # 填写你的wv向量路径
    w2vtrain = np.load('wv300_win100.train.npy')
    w2vtest = np.load('wv300_win100.test.npy')

    wv_gender_traindatas, wv_genderlabel = preprocessob.removezero(w2vtrain, labels_list_transform)
    print('预处理结束')
    pre_time_end = time.time()
    print('total time is', pre_time_end - pre_time_start)
    if order=='test':
        termob1 = classify.term()
        # termob2 = classify.term()
        # termob3 = classify.term()
        p1 = multiprocessing.Process(target=termob1.validation,
                                     args=(gender_traindatas, genderlabel, wv_gender_traindatas, 'category'))

        p1.start()
        # p2.start()
        # p3.start()

        p1.join()
        # p2.join()
        # p3.join()
    elif order=='predict':
        termob = classify.term()
        gender=termob.predict(gender_traindatas, genderlabel, testdata, wv_gender_traindatas, w2vtest, 'gender')
        '''
        /Users/Apple/datadata/sougoudata_ori/user_tag_query.10W.TRAIN.csv
        '''
        # ID = pd.read_csv('user_tag_query.10W.TEST.csv').ID
        # output('submit.csv', ID, age, gender, edu)


    end=time.time()
    print('total time is', end-start)
