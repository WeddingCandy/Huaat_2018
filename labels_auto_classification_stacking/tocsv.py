# coding=utf-8
"""
add变量表示了原始文件的路径，TRAIN/TEST
csvfile表示了生成文件的信息
主要功能：把原始文件转为UTF-8格式
注意路径
"""
import csv
import code

# add = '/Volumes/d/data/sougoudata_ori/user_tag_query.10W.TRAIN' #path of the original train file
#
# csvfile = open(add + '.csv', 'w',encoding='gb18030')# the path of the generated train file
# writer = csv.writer(csvfile)
# writer.writerow(['ID', 'age', 'Gender', 'Education', 'QueryList'])
# with open(add, 'r',encoding='gb18030') as f:
#     for line in f:
#         line.strip()
#         data = line.split("\t")
#         writedata = [data[0], data[1], data[2], data[3]]
#         querystr = ''
#         data[-1]=data[-1][:-1]#最后一个是\n，所以【：-1】指的是取到这个string最后一个元素之前
#         # print(data)
#         for d in data[4:]:
#            try:
#                 querystr += d + '\t'
#            except:
#                print(data[0],querystr)
#         querystr = querystr[:-1]
#         writedata.append(querystr)
#         writer.writerow(writedata)
#
# print('done')
add = '/Volumes/d/data/sougoudata_ori/user_tag_query.10W.TEST'#path of the original test file

csvfile = open(add + '.csv', 'w',encoding='gb18030')# the path of the generated test file
writer = csv.writer(csvfile)
writer.writerow(['ID', 'QueryList'])
with open(add, 'r',encoding='gb18030') as f:
    for line in f:
        data = line.split("\t")
        writedata = [data[0]]
        querystr = ''
        data[-1]=data[-1][:-1]
        for d in data[1:]:
           try:
                querystr +=d+ '\t' #d.decode('GB18030').encode('utf8') +
           except:
               print(data[0],querystr)
        querystr = querystr[:-1]
        writedata.append(querystr)
        writer.writerow(writedata)
