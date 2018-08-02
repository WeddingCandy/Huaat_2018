# -*- coding:UTF-8 -*
#!/usr/bin/python
"""
DATE:08/05/2018
V2.4
1.向量化处理
"""

from gensim import utils
import re
import datetime
import pandas as pd
import numpy as np
from gensim.models import doc2vec as d2v
from sklearn import metrics
import os
import sys
import random
from gensim.utils import simple_preprocess
from sklearn.model_selection import KFold




# path_docs = r'C:\Users\thinkpad\Desktop\crawlers\labels\docs'
# path_main = r'C:\Users\thinkpad\Desktop\crawlers\labels' # in ThinkPad
path_main = '/Users/Apple/datadata/labels' #in Mac
doc_label_list = r'level1_lablelist.txt'
doc_labeled = 'level1_labled.txt'
doc_fenci = 'level1_fenci.txt'
doc_test = 'test_labels_level1.txt'
doc_test_labels = 'test_labels_level1_with_label.txt'
# model_path = r'C:\Users\thinkpad\Desktop\crawlers\labels\level1_doc_train.model' # in ThinkPad

# sources = { '/Volumes/Macintosh HD/Users/RayChou/Downloads/情感分析训练语料/neg_train.txt':'TRAIN_NEG', }
files = '/Users/Apple/datadata/labels/output_tmp'
files_test = '/Users/Apple/datadata/labels/output_test'


def get_dataset(filename):
    LabeledLineSentence = d2v.TaggedLineDocument


def get_namedict(path):
    name_dict={}
    for root, dirs, files in os.walk(path):
        random.shuffle(files)
        for file in files:
            if file != '.DS_Store':
                pattern = re.compile('\.txt')
                classification = pattern.sub('',os.path.join(file))
                filename = os.path.join(root+os.sep+file)
                name_dict[filename] = classification
            else:
                 pass
    print('get name dict')
    return name_dict

def get_namelist(path):
    name_dict = []
    for root, dirs, files in os.walk(path):
        for file in files:
            ace = []
            if file != '.DS_Store':
                pattern = re.compile('\.txt')
                classification = pattern.sub('',os.path.join(file))
                filename = os.path.join(root+os.sep+file)
                ace.append(classification)
                ace.append(filename)
                name_dict.append(ace)
            else:
                 pass
    print('get name list')
    return name_dict


def classification_extract(str):
    pattern = re.compile('_[0-9]+')
    str = pattern.sub('',str)
    return str

def read_corpus(fname, tokens_only=False):
    namelist = get_namedict(fname)
    for i,key in enumerate(namelist) :
        file = key
        classification = classification_extract(namelist[key])
        # classification = str(i)
        with open(file, 'r',encoding="utf-8") as f:
            try:
                contents = f.readlines()
                for line in contents:
                    if tokens_only:
                        yield simple_preprocess(line.strip())
                    else:
                            # For training data, add tags
                        line_split = line.strip().split(' ')
                        yield d2v.TaggedDocument(line_split, [classification])
            except Exception as e:
                print(e)
                continue

def get_testset(mode):
    test_lines = []
    if mode == 'test_without_labels':
        # only input test sentences  without labels
        with open(path_main +os.sep +doc_test, 'r', encoding='utf-8') as infile:
            line = infile.readlines()
            for x in line:
                nums = len(x)
                y = x.strip().split(' ', maxsplit=nums)
                test_lines.append(y)
        return test_lines
    elif mode == 'test_with_labels':
        # input test sentences  with labels
        with open(path_main + os.sep+doc_test_labels, 'r', encoding='utf-8') as infile:
            line = infile.readlines()
            for test_sentence in line:
                test_sentence = test_sentence.strip().split('\t')
                test_lines.append(test_sentence)
        return test_lines

def get_labels_list(filename):
    label_list = {}
    with open(path_main+os.sep+ filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            label_list[i] = line.strip().replace(r'\n','')
    return label_list

def load_trainset(fname):
    name_dict = get_namedict(fname)
    whole_train_set = read_corpus(name_dict)
    file_list =[]
    classification_list = []
    for i , key in enumerate(name_dict):
        file_list.append(key)
        classification_list.append(classification_extract(name_dict[key]))
    # random.seed(20)
    # random.shuffle(file_list)
    # random.seed(20)
    # random.shuffle(classification_list)
    X = np.array(file_list)
    y = np.array(classification_list)
    return X ,y ,whole_train_set

def get_validation_set(fname):
    name_dict = get_namedict(fname)
    classification_list = []
    contents_list = []
    for i , key in enumerate(name_dict):
        with open(key, 'r', encoding="utf-8") as f:
            contents = f.readlines()
            for line in contents:
                line_split = line.strip().split()
                # print(line_split)
                # For training data, add tags
                if len(line_split) > 1:
                    contents_list.append(line_split)
                    classification_list.append(classification_extract(name_dict[key]))
                else:
                    pass
    classification_list_choice = classification_list[0:9000]
    contents_list_choice = contents_list[0:9000]
    return classification_list_choice,contents_list_choice

def merge_categories_to_whole_set(path):
    COUNT = 1
    name_list = get_namelist(path)
    init_catogery = 'null'
    list_tmp_to_store_sample = []
    output = []
    for i, line in enumerate(name_list):
        # print(i)
        classification = classification_extract(line[0])
        file = line[1]
        if classification != init_catogery :
            list_tmp_to_store_sample_tmp = list_tmp_to_store_sample
            # random.shuffle(list_tmp_to_store_sample)
            list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample) #random.shuffle
            list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
            # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
            # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
            # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
            # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
            # list_tmp_to_store_sample_tmp.remove(None)
            # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
            if COUNT > 1 :
                # list_tmp_to_store_sample_tmp.remove(None)
                output.append(d2v.TaggedDocument(list_tmp_to_store_sample_tmp, [init_catogery]))
            COUNT += 1
            list_tmp_to_store_sample_tmp = []
            init_catogery = classification
            list_tmp_to_store_sample = []
        # print(init_catogery,classification)
        if classification == init_catogery:
            with open(file, 'r',encoding="utf-8") as f:
                try:
                    contents = f.readline()
                    # For training data, add tags
                    line_split = contents.split()
                    if len(line_split) > 1 :
                        list_tmp_to_store_sample.extend(line_split)
                    else:
                        pass
                    continue
                except Exception as e:
                    print(e)
                    continue
    list_tmp_to_store_sample_tmp = list_tmp_to_store_sample
    # random.shuffle(list_tmp_to_store_sample)
    list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
    list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
    # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
    # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
    # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
    # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
    # list_tmp_to_store_sample_tmp.remove(None)
    # list_tmp_to_store_sample_tmp.extend(list_tmp_to_store_sample)
    # list_tmp_to_store_sample_tmp.remove(None)
    output.append(d2v.TaggedDocument(list_tmp_to_store_sample_tmp, [init_catogery]))
    return output



if __name__=='__main__':
    print('ok')

    run = 'ok'
    if run == 'ok':
        time = datetime.datetime.now()
        time = time.strftime("%m-%d-%H-%M-%S")
        model_path = '/Users/Apple/datadata/labels/models/level1_doc_train_{}.model'.format(time)
        x = merge_categories_to_whole_set(files)
        print(len(x))
        # with open('/Users/Apple/Desktop/check.txt','w',encoding='utf-8') as f :
        #     for i in x:
        #         f.write(str(i))
        model = d2v.Doc2Vec(min_count=3,alpha=0.02, min_alpha=0.015, window=8,
                            size=200, sample=1e-4, negative=6,workers=8)
        start_time_all = datetime.datetime.now()
        for i in range(1):
            start_time = datetime.datetime.now()
            print(i)
            random.shuffle(x)
            if i == 0:
                model.build_vocab(x)
                model.train(x, total_examples=model.corpus_count, epochs=10)  # ,start_alpha=0.02,end_alpha=0.015
                end_time = datetime.datetime.now()
                print(end_time - start_time,'s')
            else:
                model.train(x, total_examples=model.corpus_count, epochs=10) #,start_alpha=0.02,end_alpha=0.015
                end_time = datetime.datetime.now()
                print(end_time - start_time,'s')
        model.save(model_path)
        end_time_all = datetime.datetime.now()
        print(end_time_all - start_time_all, 's')
        print('model saved')
    elif run == 'valid':
        model = d2v.Doc2Vec.load('/Users/Apple/datadata/labels/models/level1_doc_train_05-09-16-05-23.model')
    # model = d2v.Doc2Vec.load('/Users/Apple/datadata/labels/models/level1_doc_train_04-25-11-41-00.model')
    # print(model.docvecs['jinrong'])
    print(model.wv.most_similar('理财', topn=5))
    print(model.wv.most_similar('工作', topn=5))
    print(model.wv.most_similar('女装', topn=5))
    mode = 'test_with_labels'
    test_lines = get_testset(mode)
    inferred_vector1 = model.infer_vector('投资')
    inferred_vector2 = model.infer_vector('旅游',
                                          alpha=0.02, min_alpha=0.01, steps=20)
    sims1 = model.docvecs.most_similar([inferred_vector1], topn=3)
    sims2 = model.docvecs.most_similar([inferred_vector2], topn=3)
    print(sims1,'\n',sims2)

    # modified_test_lines = []
    # modified_test_lines_labels = []
    # for i,line in enumerate(test_lines):
    #     if len(line) > 1 :
    #         if len(line[1])>5: #could adjust
    #             modified_test_lines.append(line[1].strip().split(' '))
    #             modified_test_lines_labels.append(line[0])
    #     else:
    #         continue
    #
    modified_test_lines_labels ,modified_test_lines= get_validation_set(files_test)
    # print(len(modified_test_lines),type(modified_test_lines_labels),modified_test_lines_labels[0:10])


    label_list = get_labels_list(doc_label_list)
    print(label_list)
    pred_labels1 = []
    pred_labels2 = []
    pred_labels3 = []
    pred_labels4 = []
    modified_test_lines_labels_tmp = []
    print(len(modified_test_lines))
    for doc_id in range(len(modified_test_lines)):
        # print(modified_test_lines[doc_id])
        inferred_vector = model.infer_vector(modified_test_lines[doc_id], alpha = 0.02, min_alpha = 0.01, steps = 10) # build vectors of test lines.
        #
        sims = model.docvecs.most_similar([inferred_vector],topn=4)
        # pred_label1 = label_list[int(sims[0][0])]
        # pred_label2 = label_list[int(sims[1][0])]
        # pred_label3 = label_list[int(sims[2][0])]
        if sims[0][1] >= 0.96 :
            modified_test_lines_labels_tmp.append(modified_test_lines_labels[doc_id])
            pred_label1 = sims[0][0]
            pred_label2 = sims[1][0]
            pred_label3 = sims[2][0]
            pred_label4 = sims[3][0]
            pred_labels1.append(pred_label1)
            pred_labels2.append(pred_label2)
            pred_labels3.append(pred_label3)
            pred_labels4.append(pred_label4)
        else:
            continue
        # print('Test Document ({},{}):<{}>\n'.format( modified_test_lines_labels[doc_id],pred_label1,' '.join(modified_test_lines[doc_id])))
        # for label,index in [('MOST',0),('MEDIAN',int(len(sims)/2+0.5)),('LAST',len(sims)-1)]:
        #     print('%s %s:<%s> \n' % (label,sims[index],'xxxxxx '))
    score1 = metrics.accuracy_score(modified_test_lines_labels_tmp, pred_labels1)
    score2 = metrics.accuracy_score(modified_test_lines_labels_tmp, pred_labels2)
    score3 = metrics.accuracy_score(modified_test_lines_labels_tmp, pred_labels3)
    score4 = metrics.accuracy_score(modified_test_lines_labels_tmp, pred_labels4)

    print(set(modified_test_lines_labels_tmp))
    print(score1,'\n',score2,'\n',score3,'\n',score4)
    print(len(modified_test_lines_labels_tmp), (len(modified_test_lines_labels_tmp) / len(modified_test_lines)) * 100)
