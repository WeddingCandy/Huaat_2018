# -*- coding:UTF-8 -*
"""
V2.1 将测试集放进单个文件中，并加入训练集中
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
from random import shuffle
from gensim.utils import simple_preprocess

path_docs = r'C:\Users\thinkpad\Desktop\crawlers\labels\docs'
# path_main = r'C:\Users\thinkpad\Desktop\crawlers\labels' # in ThinkPad
path_main = '/Volumes/d/data/labels/' #in Mac
doc_label_list = r'level1_lablelist.txt'
doc_labeled = 'level1_labled.txt'
doc_fenci = 'level1_fenci.txt'
doc_test = 'test_labels_level1.txt'
doc_test_labels = 'test_labels_level1_with_label.txt'
# model_path = r'C:\Users\thinkpad\Desktop\crawlers\labels\level1_doc_train.model' # in ThinkPad

# sources = { '/Volumes/Macintosh HD/Users/RayChou/Downloads/情感分析训练语料/neg_train.txt':'TRAIN_NEG', }
output = '/Volumes/d/data/labels/output'
output_test = '/Volumes/d/data/labels/output_test'
doc_test_labels_preprocess = 'test_labels_level1_with_label_preprocess.txt'

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

def get_namelist(path):
    namelist={}
    for root, dirs, files in os.walk(path):
        for file in files:
            pattern = re.compile('\.txt')
            classfication = pattern.sub('',os.path.join(file))
            filename = os.path.join(root+os.sep+file)
            namelist[filename] = classfication

    return namelist

def classification_extract(str):
    pattern = re.compile('_[0-9]+')
    str = pattern.sub('',str)
    return str



def read_corpus(fname, tokens_only=False):
    namelist = get_namelist(fname)
    for i,key in enumerate(namelist) :
        file = key
        classification = classification_extract(namelist[key])
        # classification = str(i)
        with open(file, 'r',encoding="utf-8") as f:
            contents = f.readlines()
            for line in contents:
                if tokens_only:
                    yield simple_preprocess(line.strip())
                else:
                        # For training data, add tags
                    line_split = line.strip().split(' ')
                    yield d2v.TaggedDocument(line_split, [classification])


def get_testset(mode):
    test_lines = []
    if mode == 'test_without_labels':
        # only input test sentences  without labels
        with open(path_main + doc_test, 'r', encoding='utf-8') as infile:
            line = infile.readlines()
            for x in line:
                nums = len(x)
                y = x.strip().split(' ', maxsplit=nums)
                test_lines.append(y)
        return test_lines
    elif mode == 'test_with_labels':
        # input test sentences  with labels
        with open(path_main + doc_test_labels, 'r', encoding='utf-8') as infile:
            line = infile.readlines()
            for test_sentence in line:
                test_sentence = test_sentence.strip().split('\t')
                test_lines.append(test_sentence)
        return test_lines





def get_labels_list(filename):
    label_list = {}
    with open(path_main+ filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            label_list[i] = line.strip().replace(r'\n','')
    return label_list


def get_testset_update_trainning(para=True):
    output_test = '/Volumes/d/data/labels/output_test'
    if para == True:
        with open(path_main + doc_test_labels, 'r', encoding='utf-8') as f:
            contents = f.readlines()
            for i,line in enumerate(contents):
                line_split=line.split()
                if len(line_split) < 5:
                    continue
                else:
                    classification_name = line_split[0]
                    content = line_split[1:-1]
                    output_file_name = output_test+os.sep+classification_name+'_'+str(i)+'.txt'
                    with open(output_file_name, 'w', encoding='utf-8') as outf:
                        outf.write(' '.join(content))
    else:
        pass


if __name__=='__main__':
    time = datetime.datetime.now()
    time = time.strftime("%m-%d-%H-%M-%S")
    model_path = '/Volumes/d/data/labels/level1_doc_train_{}.model'.format(time)

    # if not os.path.exists(model_path):
        # sentencess =  LabeledLineSentence
        # train_list = get_namelist(train_path)
    # sentences = d2v.TaggedLineDocument(path_main+doc_labeled)
    sentences = list(read_corpus(output))
    sentences_test = list(read_corpus(output_test))
    sentences.extend(sentences_test)
    print(sentences_test)
    # testset_tranning = get_testset_update_trainning(True)
    # sentences.extend(testset_tranning)
    # print(testset_tranning)
    model = d2v.Doc2Vec(min_count=1,alpha=0.02, min_alpha=0.015, window=100,
                        size=150, sample=1e-4, negative=6,workers=8)
    model.build_vocab(sentences)
    model.train(sentences, total_examples=model.corpus_count, epochs=120) #,start_alpha=0.02,end_alpha=0.015

    """
    documents (iterable of iterables) – The documents iterable can be simply a list of TaggedDocument elements, but for 
    larger corpora, consider an iterable that streams the documents directly from disk/network. If you don’t supply 
    documents, the model is left uninitialized – use if you plan to initialize it in some other way.
    """

    # model = d2v.Doc2Vec(sentences,min_count=2,alpha=0.02, min_alpha=0.015, window=60,
    #                     size=180, sample=1e-4, negative=5,iter=5, workers=8)
    model.save(model_path)
    # test_model_file1 = '/Volumes/d/data/labels/level1_doc_train_04-25-12-16-14.model'
    # test_model_file2 = '/Volumes/d/data/labels/level1_doc_train.model'
    # model = d2v.Doc2Vec.load(test_model_file1)
    # xx = model.wv.vocab
    # vocabulary = model.build_vocab(sentences)
    # print(xx)

    """
    用测试集更新训练集
    """
    # model.build_vocab(sentences_test,update=True)
    # model.train(sentences_test,total_examples=model.corpus_count,epochs=5)
    print(model.wv.most_similar('金融'))



    # test_lines = np.zeros()
    mode = 'test_with_labels'
    test_lines = get_testset(mode)


    modified_test_lines = []
    modified_test_lines_labels = []
    for i,line in enumerate(test_lines):
        if len(line) > 1 :
            if len(line[1])>2: #could adjust
                modified_test_lines.append(line[1].strip().split(' '))
                modified_test_lines_labels.append(line[0])
        else:
            continue



    label_list = get_labels_list(doc_label_list)
    # print(label_list)
    pred_labels =[]
    for doc_id in range(len(modified_test_lines)):
        inferred_vector =model.infer_vector(modified_test_lines[doc_id]) # build vectors of test lines.
        sims = model.docvecs.most_similar([inferred_vector],topn=5)

        pred_label = sims[0][0]
        pred_labels.append(pred_label)
        # print(sims)
        # print('Test Document ({},{}):<{}>\n'.format( modified_test_lines_labels[doc_id],pred_label,' '.join(modified_test_lines[doc_id])))
        # for label,index in [('MOST',0),('MEDIAN',int(len(sims)/2+0.5)),('LAST',len(sims)-1)]:
        #     print('%s %s:<%s> \n' % (label,sims[index],'xxxxxx '))
    score = metrics.accuracy_score(modified_test_lines_labels,pred_labels)
    print(score)
