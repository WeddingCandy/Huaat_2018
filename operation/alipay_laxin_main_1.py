# -*- coding: utf-8 -*-
"""
@CREATETIME: 2018/8/2 16:50 
@AUTHOR: Chans
@VERSION: 1.0
"""
import pandas as pd
match_info =  '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/match_info.xlsx'
pd_match_info = pd.read_excel(match_info,encoding = 'utf-8',header=0)
columns_match_info = ['销售代表编码', '销售代表名称', '营业员手机号', '支付宝账号认证人', '营业员绑定支付宝', 'UID']
pd_match_info_all = pd_match_info[columns_match_info]

