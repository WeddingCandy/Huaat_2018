# -*- coding:UTF-8 -*

import jieba as jb
import re
from jieba import posseg as pg
import pandas as pd
import numpy as np
from gensim.models import word2vec as w2v
import multiprocessing
import os

# path = r"C:\Users\thinkpad\Desktop\crawlers\labels\level1_result.xlsx"
path = r"C:\Users\thinkpad\Desktop\crawlers\labels\labels_testset_1.xlsx"
# path_out = r"C:\Users\thinkpad\Desktop\crawlers\labels\level1_result.xlsx"
path_out = r"C:\Users\thinkpad\Desktop\crawlers\labels\labels_testset_2.xlsx"
model_outputpath = r"C:\Users\thinkpad\Desktop\crawlers\labels\level1.model"

##结巴分词
def line_to_words(s):
    strxx = " "
    if s=='NULL' or s=='NaN':
        strxx=""
    else:
        line = pg.cut(s,HMM=False)
        allowPOS = ['n', 'v', 'a', 'ns', 'ad', 't', 's', 'vn', 'nr', 'nt']
        for word in line:
            if word.flag in allowPOS:
                strxx += word.word +" "
    # strx=" ".join(word for word in line)
    return strxx

def merge_line(data):
    length = len(data)
    x = data.iloc[:,-1:].values
    y =x.tolist()
    strxx = ''
    for line in y:
        # strxx +=" ".join(line)
        # print(line)
        yield [line.split(' ')]
    # return strxx

def yield_line(data):
    x = data.iloc[:,-1:].values
    y =x.tolist()
    return  y

def clearify_words(line):
    if line is None or line =='nan' or line =='NULL' :
        # print(line)
        x =  'OUT'
    else:
        pattern =re.compile('[0-9,，（）\(\)、。]+')
        x = pattern.sub(' ',line)
    return x


def w2v_train(s,model_outputpath):
    model = w2v.Word2Vec(s,size=150,window=5,min_count=2,workers=4)
    model.save(model_outputpath)
    print('model saved')
    return model


class textloader(object):
    def __init__(self):
        pass
    def __iter__(self):
        input=open(r"C:\Users\thinkpad\Desktop\crawlers\labels\level1_result2.txt",'r')
        for line in range(len(input.readlines())):

            line=str(input.readline())
        # segments = line.split(' ')
            yield line.split(' ')



model_path = r"C:\Users\thinkpad\Desktop\crawlers\labels\level1.model"

if not os.path.exists(model_path):
    data = pd.read_excel(path, sheet_name='Sheet1', header=0, encoding='utf-8')
    data['output'] = 'xx' #初始分词列
    for i in range(len(data)):
        line = (data.loc[i:i, "label_contents"].values).tolist()[0]
        data.loc[i:i, "output"] = line_to_words(line)
    # data.to_excel(r'C:\Users\thinkpad\Desktop\crawlers\labels\level1_fenci.xlsx',encoding='utf-8')
    aim = merge_line(data)
    se = w2v.LineSentence(r"C:\Users\thinkpad\Desktop\crawlers\labels\level1_result2.txt")
    xx = open(r"C:\Users\thinkpad\Desktop\crawlers\labels\level1_result.txt", 'w', encoding='utf-8')
    xx.write(aim)
    xx.close()
    model = w2v_train(se,model_outputpath)




model2 = w2v.Word2Vec.load(model_path)

"""
载入新的标签，加载进model更新
"""
data = pd.read_excel(path, sheet_name='Sheet1', header=0, encoding='utf-8')
data['output'] = 'xx'  # 初始分词列
xx = open(r"C:\Users\thinkpad\Desktop\crawlers\labels\test_level1_result.txt", 'w', encoding='utf-8')
for i in range(len(data)):
    line =str((data.loc[i:i, "label_contents"].values).tolist()[0])
    # print(line)
    line = clearify_words(line)
    fenci = line_to_words(line)
    data.loc[i:i, "output"] = line_to_words(line)
    xx.write(fenci+'\n')
xx.close()

yy = open(r"C:\Users\thinkpad\Desktop\crawlers\labels\level1_result.txt", 'r', encoding='utf-8')
sentence1 = yy.readlines()
model2 =w2v.Word2Vec.load(model_outputpath )
model3.train(sentence1,total_examples=1400,epochs=5,word_count=0)


print('done')

