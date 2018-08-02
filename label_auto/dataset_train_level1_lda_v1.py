# -*- coding:UTF-8 -*
#!/usr/bin/python
"""
DATE:08/05/2018
V1
1.使用LDA
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
from pprint import pprint
from gensim.utils import simple_preprocess
from gensim import corpora, models, similarities
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
    classification_list_choice = classification_list[0:1000]
    contents_list_choice = contents_list[0:1000]
    return classification_list_choice,contents_list_choice

def merge_categories_to_whole_set(path):
    COUNT = 1
    name_list = get_namelist(path)
    init_catogery = 'null'
    list_tmp_to_store_sample = []
    # output = []
    for i, line in enumerate(name_list):
        file = line[1]

        with open(file, 'r',encoding="utf-8") as f:
            try:
                contents = f.readline()
                # For training data, add tags
                line_split = contents.split()
                if len(line_split) > 1 :
                    list_tmp_to_store_sample.append(line_split)
                continue
            except Exception as e:
                print(e)
                continue
    return list_tmp_to_store_sample



if __name__=='__main__':
    print('ok')

    run = 'ok'
    if run == 'ok':
        time = datetime.datetime.now()
        time = time.strftime("%m-%d-%H-%M-%S")
        model_path = '/Users/Apple/datadata/labels/models/level1_doc_train_{}.model'.format(time)
    texts = merge_categories_to_whole_set(files)
    dictionary = corpora.Dictionary(texts)
    print(dictionary)
    V = len(dictionary)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpus_tfidf = models.TfidfModel(corpus)[corpus]

    '''
        corpora:创建字典
        corpora.Dictionary() 主要将一个array对象转换成字典
        corpora.add_documents() 补充新的文档到字典中
        doc2bow() 获得每一篇文档对应的稀疏向量,变成词袋，分别为id和出现次数
        a = models.TfidfModel(corpus) 使用tf-idf模型得出该评论集的tf-idf模型
        b = a[corpus]  此处已经计算得出所有评论的tf-idf 值
    '''
    '''
     models.LsiModel()   文档相似度
     print_topics()  输出一共有的主题,设定主题词后会得出主要的词以及权重系数
     similarities.MatrixSimilarity()
     '''
    print('\nLSI Model:')
    lsi = models.LsiModel(corpus_tfidf, num_topics=12, id2word=dictionary)
    topic_result = [a for a in lsi[corpus_tfidf]]
    # pprint(topic_result)
    print('LSI Topics:')
    pprint(lsi.print_topics(num_topics=12, num_words=100))
    # similarity = similarities.MatrixSimilarity(lsi[corpus_tfidf])   # similarities.Similarity()
    # print('Similarity:')
    # pprint(list(similarity))
