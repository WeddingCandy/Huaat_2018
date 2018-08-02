# -*- coding: utf-8 -*-
"""
@CREATETIME: 06/06/2018 08:07 
@AUTHOR: Chans
@VERSION: 
"""

import re
import pandas as pd
import os
import numpy as np





path_from =  '/Users/Apple/Desktop/working/8 华院项目/email_addr/tmp_result'
path_result = '/Users/Apple/Desktop/working/8 华院项目/email_addr/result/xxxx.csv'
#
#
for root ,c,files in os.walk(path_from):
    for file in files :
        if file == '.DS_Store':
            continue
        xx = root + os.sep + file
        print(xx)
        with open(xx,'r',encoding='utf-8') as f:
            data = f.readlines()


        with open(path_result,'a',encoding='utf-8') as ff :
            ff.writelines(data)

#
#
#
#
#
#
