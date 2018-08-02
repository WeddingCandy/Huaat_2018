# -*- coding:UTF-8 -*
#!/usr/bin/python
"""
DATE:03/05/2018
V2.3
1.随机载入写入样本集；
2.统计词数和词频
3.将每类独占词提取出
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
files = '/Users/Apple/datadata/labels/output'

def get_dataset(filename):
    LabeledLineSentence = d2v.TaggedLineDocument

# def get_namelist(path):
#     # namelist={}
#     nameList=[]
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             # pattern = re.compile('\.txt') #if needed classifications in the end ,use this .
#             # classfication = pattern.sub('',os.path.join(file))
#             filename = os.path.join(root+os.sep+file)
#             nameList.append(filename)
#             # namelist[filename] = classfication
#     nameList = nameList[1:-1]
#     return nameList

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
    classification_list_choice = classification_list[0:2000]
    contents_list_choice = contents_list[0:2000]
    return classification_list_choice,contents_list_choice






if __name__=='__main__':
    run = 'ok'
    if run == 'ok':
        time = datetime.datetime.now()
        time = time.strftime("%m-%d-%H-%M-%S")
        model_path = '/Users/Apple/datadata/labels/models/level1_doc_train_{}.model'.format(time)


        # sentencess =  LabeledLineSentence
        # train_list = get_namelist(train_path)
        # sentences = d2v.TaggedLineDocument(path_main+doc_labeled)
        sentences = list(read_corpus(files))
        model = d2v.Doc2Vec(min_count=2,alpha=0.01, min_alpha=0.001, window=30,
                            size=180, sample=1e-4, negative=6,workers=8)
        kf = KFold(n_splits=2)
        start_time_all = datetime.datetime.now()
        for i in range(10):
            start_time = datetime.datetime.now()
            print(i)
            random.shuffle(sentences)
            # print(sentences[0:10])
            # train_index, test_index =  kf.split(sentences)
            if i == 0:
                model.build_vocab(sentences)
                model.train(sentences, total_examples=model.corpus_count, epochs=20)  # ,start_alpha=0.02,end_alpha=0.015
                end_time = datetime.datetime.now()
                print(end_time - start_time,'s')
            else:
                model.train(sentences, total_examples=model.corpus_count, epochs=20) #,start_alpha=0.02,end_alpha=0.015
                end_time = datetime.datetime.now()
                print(end_time - start_time,'s')
        model.save(model_path)
        end_time_all = datetime.datetime.now()
        print(end_time_all - start_time_all, 's')
        print('model saved')
    # model = d2v.Doc2Vec.load('/Users/Apple/datadata/labels/models/level1_doc_train_05-08-15-44-27.model')
    # model = d2v.Doc2Vec.load('/Users/Apple/datadata/labels/models/level1_doc_train_04-25-11-41-00.model')

    print(model.wv.most_similar('金融', topn=5))
    print(model.wv.most_similar('租房', topn=5))
    mode = 'test_with_labels'
    test_lines = get_testset(mode)


    #
    # modified_test_lines = []
    # modified_test_lines_labels = []
    # for i,line in enumerate(test_lines):
    #     if len(line) > 1 :
    #         if len(line[1])>5: #could adjust
    #             modified_test_lines.append(line[1].strip().split(' '))
    #             modified_test_lines_labels.append(line[0])
    #     else:
    #         continue

    modified_test_lines_labels ,modified_test_lines= get_validation_set(files)
    print(len(modified_test_lines),type(modified_test_lines_labels),modified_test_lines_labels[0:10])


    label_list = get_labels_list(doc_label_list)
    print(label_list)
    pred_labels1 = []
    pred_labels2 = []
    pred_labels3 = []
    for doc_id in range(len(modified_test_lines)):
        # print(modified_test_lines[doc_id])
        inferred_vector = model.infer_vector(modified_test_lines[doc_id], alpha=0.2, min_alpha=0.1, steps=10) # build vectors of test lines.
        sims = model.docvecs.most_similar([inferred_vector],topn=3)
        # pred_label1 = label_list[int(sims[0][0])]
        # pred_label2 = label_list[int(sims[1][0])]
        # pred_label3 = label_list[int(sims[2][0])]
        pred_label1 = sims[0][0]
        pred_label2 = sims[1][0]
        pred_label3 = sims[2][0]
        pred_labels1.append(pred_label1)
        pred_labels2.append(pred_label2)
        pred_labels3.append(pred_label3)
        # print('Test Document ({},{}):<{}>\n'.format( modified_test_lines_labels[doc_id],pred_label,' '.join(modified_test_lines[doc_id])))
        # for label,index in [('MOST',0),('MEDIAN',int(len(sims)/2+0.5)),('LAST',len(sims)-1)]:
        #     print('%s %s:<%s> \n' % (label,sims[index],'xxxxxx '))
    score1 = metrics.accuracy_score(modified_test_lines_labels, pred_labels1)
    score2 = metrics.accuracy_score(modified_test_lines_labels, pred_labels2)
    score3 = metrics.accuracy_score(modified_test_lines_labels, pred_labels3)
    print(score1,'\n',score2,'\n',score3)
