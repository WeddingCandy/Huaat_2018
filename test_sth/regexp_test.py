# -*- coding: utf-8 -*-
"""
@CREATETIME: 06/06/2018 08:07
@AUTHOR: Chans
@VERSION:
"""

import re
import pandas as pd
import os
import time




# file_path_in = '/data/hive_data/data_data/email_addar.csv'
# file_path_out = '/data/hive_data/data_data/output.csv'
file_path_in = '/Users/Apple/Desktop/working/8 华院项目/email_addr/email_addar_details.csv'
file_path_out = '/Users/Apple/Desktop/working/8 华院项目/email_addr/output.csv'
result_out = '/Users/Apple/Desktop/working/8 华院项目/email_addr/tmp_result'
doc_out = '/Users/Apple/Desktop/working/8 华院项目/email_addr/tmp_save'
data = pd.read_csv(file_path_in,header=None,names=['imei','addr','pdate','pregion'],sep='\t')

for root ,c,files in os.walk(doc_out):

    print( i for i in files)

length = int(len(data.index))

x = length % 50000
y = length// 50000 +1
print(data.info())
print(length,x,y)

# model = 'split'
model = 'process'
if model == 'split':
    for i in range(y):
        # print(i)
        if i ==0  :
            index1 = 50000 * i
            index2 = 50000 * (1 + i)
        elif 0<i<y-1:
            index1 = 1+ 50000 * i
            index2 = 50000 * (1 + i)
        else :
            index1 = 1+ 50000 * i
            index2 = 50000 * (1 + i) +x

        print(index1,index2)
        data_out = data[index1:index2]
        # print(data_out)
        filename = doc_out + os.sep + 'split_{}_to_{}.csv'.format(index1,index2)
        print(filename)
        data_out.to_csv(filename,sep=",",header=False,index=False,encoding='utf-8')

elif model == 'process':
    def matchh(x):
        if len(x) == 11:
            pattern1 = re.compile('^([0-9][0-9]{10})$')
            a = pattern1.match(x)
            return a
        else:
            pattern2 = re.compile('^([a-z][a-z_0-9]+)$')
            y = pattern2.match(x)
            return y

    for root ,c,files in os.walk(doc_out):

        for index,i in enumerate(files):
            if i == '.DS_Store':
                continue
            file_name = root+os.sep+i
            print(file_name)
            start_time = time.time()
            data = pd.read_csv(file_name,header=None,names=['imei','addr','pdate','pregion'])

            length = int(len(data.index))
            COUNT = 0
            for i in range(length):
                xx = data.ix[i:i, 1:2].values[0][0]
                # print('now is %d' % (i),xx)
                y = matchh(xx)
                if y is None:
                    data = data.drop(i)
                    continue
                elif y.group() == 'unknown' :
                    data = data.drop(i)
                    continue
                else:
                    COUNT += 1
                    # print(xx)
            total_time = time.time() - start_time
            print(index)
            print('Total valid id is: %d and spent time is %s .' % (COUNT,total_time) )
            result_name = result_out+ os.sep + '{}.csv'.format(index)
            data.to_csv(result_name, index=False, sep=',', encoding='utf-8')
    print('done')
