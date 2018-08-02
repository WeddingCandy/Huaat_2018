# -*- coding: utf-8 -*-
"""
@CREATETIME: 2018/8/2 16:50 
@AUTHOR: Chans
@VERSION: 1.0
"""
import pandas as pd
match_info =  '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/match_info.xlsx'
pd_match_info = pd.read_excel(match_info,encoding = 'utf-8',header=0)
pd_match_info = pd_match_info.iloc[:,1:]