# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
import os

def read_match_info(file):
    pd_match_info = pd.read_excel(file,encoding = 'utf-8',header=0)
    columns_match_info = ['销售代表编码', '销售代表名称', '营业员手机号', '支付宝账号认证人', '营业员绑定支付宝', 'UID']
    pd_match_info_aim = pd_match_info[columns_match_info]
    return pd_match_info_aim

def read_detail(file):
    pd_detail = pd.read_excel(file,encoding = 'utf-8',header=0)
    return  pd_detail

def search_new_input_file(file_path):
    import os
    import re
    import datetime
    date = (datetime.date.today() ).strftime('%m%d') #+ datetime.timedelta(days = -1)

    all_files = []
    aim_file =''
    for root, dirs, files in os.walk(file_path):
        all_files = files
    print(all_files,date)
    pattern1 = '[\w-]+{}\.xlsx'.format(date)
    # print(pattern1)
    reg_exp = re.compile(pattern1)
    for file in all_files:
        if len(reg_exp.findall(file))>0 :
            aim_file =reg_exp.findall(file)[0]
    print(aim_file)
    return aim_file

def connection_with_match_info(dataframe,dataframe_info):
    dataframe_info.drop_duplicates(dataframe_info.columns.tolist(),keep='first',inplace=True)
    pd_detail = dataframe.merge(dataframe_info[['销售代表编码', 'UID']], how='left', left_on='商户编码', right_on='销售代表编码')
    pd_detail.rename(columns={ 'UID': '商户对应UID','销售代表编码_x':'销售代表编码'}, inplace=True)
    print(pd_detail.head())
    pd_detail = pd_detail.drop(['销售代表编码_y'], axis=1)
    pd_detail = pd_detail.merge(dataframe_info[['销售代表编码', 'UID','销售代表名称','营业员绑定支付宝']], how='left', left_on='销售代表编码', right_on='销售代表编码')
    print(pd_detail.head())
    pd_detail.rename(columns={'UID': '销售代表对应UID','销售代表编码_x':'销售代表编码',
                              '销售代表名称_x':'销售代表名称','销售代表名称_y':'销售代表打款支付宝账户认证人',
                             '营业员绑定支付宝':'销售代表打款支付宝账户'}, inplace=True)
    return pd_detail

def get_vacant_index(dataframe,line_name):
    index = dataframe[dataframe[line_name].isnull().values == False].index.tolist()
    return index


def write_index_line(dataframe,index,aim_line,from_line):
    dataframe[aim_line][index] = dataframe[from_line][index]
    return dataframe

def create_new_line(dataframe,line_name):
    dataframe[line_name] = np.nan
    return dataframe

def get_position_index(dataframe,line_index):
    index = dataframe[dataframe.iloc[:, line_index].isnull().values == True].index.tolist()
    return index


def output_uid(dataframe,indexx):
    for content in range(indexx):
        if (dataframe['商户对应UID'][content] is not np.nan ) & (dataframe['销售代表对应UID'][content] is not np.nan ) == True:
            dataframe['打款账户'][content] = dataframe['商户编码'][content]
        elif (dataframe['商户对应UID'][content] is not np.nan ) & (dataframe['销售代表对应UID'][content] is np.nan ) == True:
            dataframe['打款账户'][content] = dataframe['商户编码'][content]
        elif (dataframe['商户对应UID'][content] is np.nan ) & (dataframe['销售代表对应UID'][content] is not np.nan) == True:
            dataframe['打款账户'][content] = dataframe['销售代表编码'][content]
        elif (dataframe['商户对应UID'][content] is np.nan ) & (dataframe['销售代表对应UID'][content] is  np.nan) == True:
            dataframe['打款账户'][content] = dataframe['营业员支付宝账户'][content]
    for index in dataframe.index :
        if (dataframe['销售代表对应UID'][index]  is not np.nan) & (dataframe['商户对应UID'][index]  is  np.nan) == True:
            dataframe['打款UID'][index] = str(dataframe['销售代表对应UID'][index])
            continue
        elif (dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is not np.nan) == True:
            dataframe['打款UID'][index] = str(dataframe['商户对应UID'][index])
            continue
        elif (dataframe['销售代表对应UID'][index]  is not np.nan) & (dataframe['商户对应UID'][index]  is not np.nan) == True:
            dataframe['打款UID'][index] = str(dataframe['商户对应UID'][index])
            continue
        elif ((dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is np.nan) & (dataframe['打款账户'][index]  is not np.nan ) )== True :
            dataframe['打款UID'][index] = str(dataframe['营业员UID'][index])
            continue
    return dataframe

def account_name_way(dataframe):
    for index in dataframe.index :
        if (dataframe['销售代表对应UID'][index]  is not np.nan) & (dataframe['商户对应UID'][index]  is  np.nan) == True:
            dataframe['打款支付宝账户'][index] = str(dataframe['销售代表支付宝账户'][index])
            dataframe['打款支付宝认证'][index] = str(dataframe['销售代表打款支付宝账户认证人'][index])
            dataframe['备注：结算方式'][index] = '销售代表'
            continue
        elif (dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is not np.nan) == True:
            dataframe['打款支付宝账户'][index] = str(dataframe['商户支付宝账户'][index])
            dataframe['打款支付宝认证'][index] = str(dataframe['商户支付宝账户认证人'][index])
            dataframe['备注：结算方式'][index] = '商户'
            continue
        elif (dataframe['销售代表对应UID'][index]  is not np.nan) & (dataframe['商户对应UID'][index]  is not np.nan) == True:
            dataframe['打款支付宝账户'][index] = str(dataframe['商户支付宝账户'][index])
            dataframe['打款支付宝认证'][index] = str(dataframe['商户支付宝账户认证人'][index])
            dataframe['备注：结算方式'][index] = '商户'
            continue
        elif ((dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is np.nan) & (dataframe['打款账户'][index]  is not np.nan ) )== True :
            dataframe['打款支付宝账户'][index] = str(dataframe['营业员支付宝账户'][index])
            dataframe['打款支付宝认证'][index] = str(dataframe['营业员支付宝账户认证人'][index])
            dataframe['备注：结算方式'][index] = '营业员'
            continue
    return dataframe


def write_to_excel_a(dataframe,output_path):
    for index in range(len(dataframe)):
        dataframe.loc[index:index, ['营业员UID']] = str(dataframe.loc[index:index,['营业员UID']].values[0][0])
        dataframe.loc[index:index, ['商户UID']] =  str(dataframe.loc[index:index, ['商户UID']].values[0][0])
        if index <3:
            print(dataframe.loc[index:index,['营业员UID']].values[0][0])
    # dataframe[['营业员UID']] = ['@%s' % d for d in dataframe[['营业员UID']]]
    # dataframe[['商户UID']] = ['@%s' % d for d in dataframe[['商户UID']]]
    dataframe.to_excel(output_path,encoding='utf-8',index=False,sheet_name=r'匹配明细')

def write_to_excel_c(dataframe,output_path):
    dataframe.to_excel(output_path,encoding='utf-8',index=True,sheet_name=r'佣金计算',merge_cells=False)

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
    today_date = datetime.datetime.now().strftime('%Y%m%d')

    for i_index in range(pd_length):
        # insert_date = dataframe.iloc[i_index:i_index+1,0:1].values
        insert_date2 = str(dataframe.loc[i_index:i_index , ['日期']].values[0][0])
        # print(dataframe.iloc[i_index:i_index+1,0:1],insert_date,insert_date2)
#         insert_date = datetime.datetime.strptime(insert_date2,'%Y-%m-%d %H:%M:%S')
#         insert_date = datetime.datetime.strftime(insert_date,'%Y%m%d')
        a = "${a}_{b}".format(a = insert_date2 ,b = dataframe['打款账户'][i_index])

        df['orderID(结算日期加营业员手机号)'][i_index] =  a
            # patten.sub('_',a)

        df['payAccount(营业员支付宝UID)'][i_index] = dataframe['打款UID'][i_index]
        df['money(发好多钱)'][i_index] = dataframe['佣金'][i_index]
        df['remark(支付描述-日期-营业员手机号)'][i_index] = '淘宝拉新奖励_{a}_{b}'.format(a = insert_date2,b = dataframe['备注：结算方式'][i_index])
    df['activityID(固定值120)'] = 120
    df['moneyType(固定值1)'] = 1
    df['status(固定值-1)'] = -1
    df.to_excel(output_path, encoding='utf-8', index=False, sheet_name=r'打款明细')
    return df
def pivot_group_by(dataframe,output_path):
    pd_output = dataframe.fillna('$')
    cols =  pd_output.columns.values.tolist()
    cols.remove('money(发好多钱)')
    y = pd.pivot_table(pd_output,index=cols,values = ['money(发好多钱)'],aggfunc=np.sum)
    write_to_excel_c(y,output_path)

if __name__ == '__main__':
    # -----paths-----
    date = datetime.datetime.now().strftime('%Y%m%d')
    match_info = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/taobao/input/match_info.xlsx'
    input_file_path = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/taobao/input'
    output_file_path = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/taobao/output'
    output_a_test = output_file_path + os.sep + '手淘拉新返点明细表_{}.xlsx'.format(date)

    file_name = search_new_input_file(input_file_path)
    detail = input_file_path + os.sep + '{}'.format(file_name)

    pd_match_info_aim = read_match_info(match_info)
    pd_detail = read_detail(detail)
    pd_detail = connection_with_match_info(pd_detail,pd_match_info_aim)


    pd_detail = create_new_line(pd_detail,'打款账户')
    index1 = get_vacant_index(pd_detail,'商户对应UID')
    index2 = get_vacant_index(pd_detail,'销售代表对应UID')
    pd_detail = write_index_line(pd_detail,index1,'打款账户','商户支付宝账户')
    pd_detail = write_index_line(pd_detail,index2,'打款账户','销售代表支付宝账户')
    pd_detail = create_new_line(pd_detail,'打款UID')


    index3 = len(pd_detail)
    pd_detail = output_uid(pd_detail,index3)

    pd_detail = create_new_line(pd_detail,'打款支付宝账户')
    pd_detail = create_new_line(pd_detail,'打款支付宝认证')
    pd_detail = create_new_line(pd_detail,'备注：结算方式')

    pd_detail = account_name_way(pd_detail)
    write_to_excel_a(pd_detail,output_a_test)

    output_b_test = output_file_path + os.sep + 'output_test_b_{}.xlsx'.format(date)
    pd_output = write_to_excel_b(pd_detail,output_b_test,pd_length=len(pd_detail))
    output_c_test = output_file_path + os.sep + '手淘拉新打款明细表_{}.xlsx'.format(date)
    pivot_group_by(pd_output,output_c_test)