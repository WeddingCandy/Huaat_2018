# -*- coding: utf-8 -*-
"""
@CREATETIME: 09/06/2018 10:01 
@AUTHOR: Chans
@VERSION: 
"""


path_in = '/Users/Apple/Desktop/working/8 华院项目/email_addr/op_qq_mail.txt'
path_out = '/Users/Apple/Desktop/working/8 华院项目/email_addr/op_qq_mail_fin.txt'
with open(path_in,'r',encoding='utf-8') as f:
    x = f.readlines()

li = []
print(x[0:3])
for ele in x:
    link = ele.strip()+'@qq.com\n'
    li.append(link)

with open(path_out,'w',encoding='utf-8') as ff:
    ff.writelines(li)

