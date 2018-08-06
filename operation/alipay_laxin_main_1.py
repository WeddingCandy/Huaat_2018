# -*- coding: utf-8 -*-
"""
@CREATETIME: 2018/8/2 16:50 
@AUTHOR: Chans
@VERSION: 2.0
"""
import pandas as pd
import numpy as np
import datetime


def read_match_info(file):
    pd_match_info = pd.read_excel(file,encoding = 'utf-8',header=0)
    columns_match_info = ['销售代表编码', '销售代表名称', '营业员手机号', '支付宝账号认证人', '营业员绑定支付宝', 'UID']
    pd_match_info_aim = pd_match_info[columns_match_info]
    return pd_match_info_aim

def read_detail(file):
    pd_detail = pd.read_excel(file,encoding = 'utf-8',header=0,sheetname='明细数据')
    return  pd_detail


def connection_with_match_info(dataframe):
    pd_detail = dataframe.merge(pd_match_info_aim[['销售代表编码', 'UID']], how='left', left_on='商户编码', right_on='销售代表编码')
    pd_detail.rename(columns={'销售代表编码_x': '销售代表编码', 'UID': '商户对应UID'}, inplace=True)
    columns = (list(pd_detail.columns))[0:-2]
    columns.extend(list(pd_detail.columns)[-1:])
    pd_detail = pd_detail[columns]

    pd_detail = pd_detail.merge(pd_match_info_aim[['销售代表编码', 'UID']], how='left', left_on='销售代表编码', right_on='销售代表编码')
    pd_detail.rename(columns={'UID': '销售代表对应UID'}, inplace=True)
    return pd_detail

def get_vacant_index(dataframe,line_name):
    index = dataframe[dataframe[line_name].isnull().values == False].index.tolist()
    return index

def get_position_index(dataframe,line_index):
    index = dataframe[dataframe.iloc[:, line_index].isnull().values == True].index.tolist()
    return index




def create_new_line(dataframe,line_name):
    dataframe[line_name] = np.nan
    return dataframe
def write_index_line(dataframe,index,aim_line,from_line):
    dataframe[aim_line][index] = dataframe[from_line][index]
    return dataframe

def output_uid(dataframe,indexx):
    for content in indexx:
        if (dataframe['商户对应UID'][content] is np.nan == False) & (dataframe['销售代表对应UID'][content] is np.nan == False) == True:
            dataframe['打款账户(营业员手机号/商户编码/销售代表编码)'][content] = dataframe['商户编码'][content]
        elif (dataframe['商户对应UID'][content] is np.nan == False) & (dataframe['销售代表对应UID'][content] is np.nan == True) == True:
            dataframe['打款账户(营业员手机号/商户编码/销售代表编码)'][content] = dataframe['商户编码'][content]
        elif (dataframe['商户对应UID'][content] is np.nan == True) & (dataframe['销售代表对应UID'][content] is np.nan == False) == True:
            dataframe['打款账户(营业员手机号/商户编码/销售代表编码)'][content] = dataframe['销售代表编码'][content]
        # elif (dataframe['商户对应UID'][content] is np.nan == True) & (dataframe['销售代表对应UID'][content] is np.nan == True) == True:
        else:
            dataframe['打款账户(营业员手机号/商户编码/销售代表编码)'][content] = dataframe['营业员手机号'][content]


    for index in dataframe.index :
        if (dataframe['销售代表对应UID'][index]  is not np.nan) & (dataframe['商户对应UID'][index]  is  np.nan) == True:
            dataframe['打款UID'][index] = 'a'+ str(dataframe['销售代表对应UID'][index])
            continue
        elif (dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is not np.nan) == True:
            dataframe['打款UID'][index] = 'a'+ str(dataframe['商户对应UID'][index])
            continue
        elif (dataframe['销售代表对应UID'][index]  is not np.nan) & (dataframe['商户对应UID'][index]  is not np.nan) == True:
            dataframe['打款UID'][index] = 'a'+ str(dataframe['商户对应UID'][index])
            continue
        elif ((dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is np.nan) & (dataframe['打款账户(营业员手机号/商户编码/销售代表编码)'][index]  is not np.nan ) )== True :
            dataframe['打款UID'][index] = 'a'+ str(dataframe['营业员支付宝UID'][index])
            continue
    return dataframe
def write_to_excel_a(dataframe,output_path):
    dataframe.to_excel(output_path,encoding='utf-8',index=False,sheet_name=r'匹配明细')

def write_to_excel_c(dataframe,output_path):
    dataframe.to_excel(output_path,encoding='utf-8',index=True,sheet_name=r'佣金计算')

def empty_dataframe(shape,columns):
    data = np.zeros(shape)
    df = pd.DataFrame(data=data, columns=columns)
    for content in columns:
        df[content]=np.nan
    return df



def write_to_excel_b(dataframe,output_path,pd_length):
    columns = ['id', 'activityID(固定值120)', 'orderID(结算日期加营业员手机号)', 'agentID', 'businessID', 'shopID', 'assistant',
               'areaCode',
               'moneyType(固定值1)', 'payAccount(营业员支付宝UID)', 'payAccountName', 'money(发好多钱)', 'status(固定值-1)',
               'couponNO1',
               'couponNO2', 'couponNO3', 'couponNO4', 'couponNO5', 'remark(支付描述-日期-营业员手机号)', 'createrId', 'createTime',
               'updaterId', 'updateTime', 'delflag', 'payNo', 'payTime', 'payDetail']
    col_length = len(columns)
    df = empty_dataframe([pd_length,col_length],columns)
    date = datetime.datetime.now().strftime('%Y%m%d')
    for i_index in range(pd_length):
        # print(i_index,'{a}_{b}'.format(a=date ,b=str(dataframe['打款账户(营业员手机号/商户编码/销售代表编码)'][i_index])))
        df['orderID(结算日期加营业员手机号)'][i_index] ='{a}_{b}'.format(a=date ,b=str(dataframe['打款账户(营业员手机号/商户编码/销售代表编码)'][i_index]))
        df['payAccount(营业员支付宝UID)'][i_index] = dataframe['打款UID'][i_index]
        df['money(发好多钱)'][i_index] = dataframe['佣金'][i_index]
        df['remark(支付描述-日期-营业员手机号)'][i_index] = '支付宝拉新奖励-{a}_{b}'.format(a=date,b=str(dataframe['打款账户(营业员手机号/商户编码/销售代表编码)'][i_index]))
    df['activityID(固定值120)'] = 120
    df['moneyType(固定值1)'] = 1
    df['status(固定值-1)'] = -1
    df.to_excel(output_path, encoding='utf-8', index=False, sheet_name=r'打款明细')
    return df

def pivot_group_by(dataframe,output_path):
    pd_output = dataframe.fillna(2)
    cols =  pd_output.columns.values.tolist()
    cols.remove('money(发好多钱)')
    y = pd.pivot_table(pd_output,index=cols,values = ['money(发好多钱)'],aggfunc=np.sum)
    write_to_excel_c(y,output_path)

if __name__ == '__main__':
    # -----paths-----
    match_info = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/match_info.xlsx'
    detail = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/test_details_0802.xlsx'
    output_a_test = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/output_test_a_0803.xlsx'
    output_b_test = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/output_test_b_0803.xlsx'
    output_c_test = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/output_test_c_0803.xlsx'
    output_test = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/output_test_0803.xlsx'


    # -----main-----
    pd_match_info_aim = read_match_info(match_info)
    pd_detail = read_detail(detail)
    pd_detail = connection_with_match_info(pd_detail)
    index1 = get_vacant_index(pd_detail,'商户对应UID')
    index2 = get_vacant_index(pd_detail,'销售代表对应UID')
    pd_detail = create_new_line(pd_detail,'打款账户(营业员手机号/商户编码/销售代表编码)')
    pd_detail = write_index_line(pd_detail,index1,'打款账户(营业员手机号/商户编码/销售代表编码)','商户编码')
    pd_detail = write_index_line(pd_detail,index2,'打款账户(营业员手机号/商户编码/销售代表编码)','销售代表编码')
    index3 = get_position_index(pd_detail,[-1,])
    pd_detail = create_new_line(pd_detail,'打款UID')
    pd_detail = output_uid(pd_detail,index3)
    write_to_excel_a(pd_detail,output_test)
    # c = ['日期', '二级pid', '数量', '单价', '佣金', '营业员姓名', '营业员手机号', '营业员支付宝账号',
    #  '营业员支付宝UID', '所属区域', '门店编码', '门店名称', '商户编码', '商户名称', '销售代表编码', '销售代表名称','属性']

    pd_output = write_to_excel_b(pd_detail,output_test,pd_length=len(pd_detail))

    pivot_group_by(pd_output,output_test)
