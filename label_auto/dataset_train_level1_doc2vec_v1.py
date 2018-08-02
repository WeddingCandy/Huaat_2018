# -*- coding:UTF-8 -*

from gensim import utils
import jieba as jb
import re
from jieba import posseg as pg
import pandas as pd
import numpy as np
from sklearn import metrics
from gensim.models import doc2vec as d2v
import multiprocessing
import os
import sys
from random import shuffle
path_docs = r'C:\Users\thinkpad\Desktop\crawlers\labels\docs'
# path_main = r'C:\Users\thinkpad\Desktop\crawlers\labels' # in ThinkPad
path_main = '/Users/Apple/datadata/labels' #in Mac
doc_label_list = r'level1_lablelist.txt'
doc_labeled = 'level1_labled.txt'
doc_fenci = 'level1_fenci.txt'
doc_test = 'test_labels_level1.txt'
doc_test_labels = 'test_labels_level1_with_label.txt'
# model_path = r'C:\Users\thinkpad\Desktop\crawlers\labels\level1_doc_train.model' # in ThinkPad
model_path = '/Volumes/d/data/labels/level1_doc_train.model'
# sources = { '/Volumes/Macintosh HD/Users/RayChou/Downloads/情感分析训练语料/neg_train.txt':'TRAIN_NEG', }
doc_test_labels_preprocess = 'test_labels_level1_with_label_preprocess.txt'

def get_namelist(path):
    namelist={}
    for root, dirs, files in os.walk(path):
        for file in files:
            pattern = re.compile('\.txt')
            classfication = pattern.sub('',os.path.join(file))
            filename = os.path.join(root+'\\'+file)
            namelist[filename] = classfication
    return namelist



class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield d2v.LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(d2v.LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

def getWordVecs(words):
    vecs = []
    for word in words:
        word = word.replace('\n', '')
        try:
            vecs.append(model[word].reshape((1, 300)))
        except KeyError:
            continue
    vecs = np.concatenate(vecs)
    return np.array(vecs, dtype='float')  # TSNE expects float type values


def GetWordVecs(line):
    vecs = []
    words = line.split(' ')
    for word in words:
        word = word.replace('\\t', '')
        try:
            vecs.append(model[word].reshape(1, 100))
        except KeyError:
            continue
    vecs = np.concatenate(vecs)
    return np.array(vecs,dtype='float')

def GetDocMeanVecs(object):
    print('Return a list which contines class and its mean vec score.')
    with open(object,'r',encoding='utf-8') as f:
        lines = f.readlines()
        class_vecs_score = np.zeros([19,2])
        class_vecs_score = class_vecs_score.tolist()
        # print(class_vecs_score)
        for i, line in enumerate(lines):
            cc = GetWordVecs(line)
            # print(cc.shape,cc.size)
            vecs_mean =(np.array(cc.sum(axis=0))).tolist()
            # print(vecs_mean)
            class_vecs_score[i] = [i,vecs_mean]
    return class_vecs_score


def get_labels_list(filename):
    label_list = {}
    with open(path_main+ filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            label_list[i] = line.strip().replace(r'\n','')
    return label_list

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

def get_testset_update_trainning(para=True):
    doc_test_labels_preprocess = 'test_labels_level1_with_label_preprocess.txt'
    if para == True:
        with open(path_main + doc_test_labels, 'r', encoding='utf-8') as f:
            contents = f.readlines()
            with open(path_main + doc_test_labels_preprocess, 'w', encoding='utf-8') as outf:
                for line in contents:
                    if len(line.strip()) < 5:
                        continue
                    else:
                        outf.write(line)
    else:
        pass

    sentences = d2v.TaggedLineDocument(path_main + doc_test_labels_preprocess)
    return sentences



if __name__=='__main__':

    # if not os.path.exists(model_path):
        # sentencess =  LabeledLineSentence
        # train_list = get_namelist(train_path)
    # sentences = d2v.TaggedLineDocument(path_main+os.sep+ doc_labeled)
    # model = d2v.Doc2Vec(sentences,min_count=2,alpha=0.020, min_alpha=0.015, window=60,
    #                      size=180, sample=1e-4, negative=6,workers=8,iter=5)
    # # # model = d2v.Doc2Vec(sentences,min_count=2,alpha=0.02, min_alpha=0.015, window=60,
    # # #                     size=180, sample=1e-4, negative=5,iter=5, workers=8)
    # model.save(model_path)

    # model = d2v.Doc2Vec.load(model_path)
    """
    获得词向量
    """

    # doc_mean_vecs = GetDocMeanVecs(path_main+doc_fenci) #[19,[100,1]]

    # print(list)

    """
    在线训练新词
    """
    #预测集的情况
    # test_lines = []
    # with open(path_main+'\\'+doc_test, 'r',encoding='utf-8') as infile:
    #     test_words = infile.readlines()
    #
    #     for x in test_words:
    #         nums = len(x)
    #         y = x.strip().split(' ',maxsplit=nums)
    #         test_lines.append(y)
    """
    用测试集更新训练集
    """
    # testset_tranning = get_testset_update_trainning(True)
    # testset_tranning2 = d2v.TaggedLineDocument(path_main+doc_test_labels_preprocess)
    # for i in testset_tranning:
    #     print(i)
    # model.train(testset_tranning2,total_examples=model.corpus_count,epochs=20)
    print(model['金融'])
    print(model.wv.most_similar('金融'))
    print(model['理财'])
    print(model.wv.most_similar('理财'))
    print(model['游戏'])
    print(model.wv.most_similar('游戏'))



    """
    测试集测试
    """


    # test_lines = np.zeros()


    mode = 'test_with_labels'
    test_lines = get_testset(mode)

    modified_test_lines = []
    modified_test_lines_labels = []
    for i,line in enumerate(test_lines):
        if len(line) > 1 :
            if len(line[1])>5: #could adjust
                modified_test_lines.append(line[1].strip().split(' '))
                modified_test_lines_labels.append(line[0])
        else:
            continue


    # parttern = re.compile('[0-9]+')
    # classfication = re.findall(parttern,y)


    label_list = get_labels_list(doc_label_list)
    # print(label_list)
    pred_labels1 = []
    pred_labels2 = []
    pred_labels3 = []
    for doc_id in range(len(modified_test_lines)):
        inferred_vector =model.infer_vector(modified_test_lines[doc_id],alpha=0.3, min_alpha=0.1, steps=20) # build vectors of test lines.
        sims = model.docvecs.most_similar([inferred_vector],topn=3)
        pred_label1 = label_list[int(sims[0][0])]
        pred_label2 = label_list[int(sims[1][0])]
        pred_label3 = label_list[int(sims[2][0])]
        pred_labels1.append(pred_label1)
        pred_labels2.append(pred_label2)
        pred_labels3.append(pred_label3)
        print('Test Document ({},{}):<{}>\n'.format( modified_test_lines_labels[doc_id],pred_label1,' '.join(modified_test_lines[doc_id])))
        # for label,index in [('MOST',0),('MEDIAN',int(len(sims)/2+0.5)),('LAST',len(sims)-1)]:
        #     print('%s %s:<%s> \n' % (label,sims[index],'xxxxxx '))
    score1 = metrics.accuracy_score(modified_test_lines_labels, pred_labels1)
    score2 = metrics.accuracy_score(modified_test_lines_labels, pred_labels2)
    score3 = metrics.accuracy_score(modified_test_lines_labels, pred_labels3)
    print(score1,'\n',score2,'\n',score3)