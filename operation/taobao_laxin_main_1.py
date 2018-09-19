# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
import os
import warnings
warnings.filterwarnings("ignore")

def read_match_info(file , columns_match_info):
    pd_match_info = pd.read_excel(file,encoding = 'utf-8',header=0)
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
    pattern1 = '[\u4e00-\u9fa5\w\s-]+{}\.xlsx'.format(date)
    reg_exp = re.compile(pattern1)
    for file in all_files:
        if len(reg_exp.findall(file))>0 :
            aim_file =reg_exp.findall(file)[0]
    print('现在执行的是文档是：' , aim_file)
    return aim_file

def connection_with_match_info(dataframe,dataframe_info):
    dataframe_info.drop_duplicates(dataframe_info.columns.tolist(),keep='first',inplace=True)
    pd_detail = dataframe.merge(dataframe_info[['销售代表编码', '支付宝账号认证人', '营业员绑定支付宝', 'UID']],
                                how='left', left_on='商户编码', right_on='销售代表编码')


    pd_detail.rename(columns={'销售代表编码_x': '销售代表编码','UID': '商户对应UID', '支付宝账号认证人': 'user_info商户支付宝账号认证人',
                              '营业员绑定支付宝': 'user_info商户支付宝' ,'销售代表编码_y':'user_info商户编码'}, inplace=True)   #
    pd_detail = pd_detail.drop(['user_info商户编码'], axis=1)

    pd_detail = pd_detail.merge(dataframe_info[['销售代表编码', '支付宝账号认证人','营业员绑定支付宝','UID']],
                                how='left', left_on='销售代表编码', right_on='销售代表编码')
    pd_detail.rename(columns={'UID': '销售代表对应UID',
                              '支付宝账号认证人': 'user_info销售代表打款支付宝账户认证人',
                                '营业员绑定支付宝':'user_info销售代表打款支付宝账户'}, inplace=True)

    print(pd_detail.columns)
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



def match_uid(dataframe,indexx):
    for content in range(indexx):
        if (dataframe['商户对应UID'][content] is not np.nan ) & (dataframe['销售代表对应UID'][content] is not np.nan ) == True:
            dataframe['打款账户'][content] = dataframe['商户编码'][content]
        elif (dataframe['商户对应UID'][content] is not np.nan ) & (dataframe['销售代表对应UID'][content] is np.nan ) == True:
            dataframe['打款账户'][content] = dataframe['商户编码'][content]
        elif (dataframe['商户对应UID'][content] is np.nan ) & (dataframe['销售代表对应UID'][content] is not np.nan) == True:
            dataframe['打款账户'][content] = dataframe['销售代表编码'][content]
        elif (dataframe['商户对应UID'][content] is np.nan ) & (dataframe['销售代表对应UID'][content] is  np.nan) == True:
            dataframe['打款账户'][content] = dataframe['营业员电话'][content]

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
        elif ((dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is np.nan)
              & (dataframe['打款账户'][index]  is not np.nan ) )== True :
            dataframe['打款UID'][index] = str(dataframe['营业员UID'][index])
            continue
    return dataframe

def remarks_supplements(dataframe):
    for index in dataframe.index :
        insert_date2 = str( dataframe['日期'][index])
        insert_date = datetime.datetime.strptime(insert_date2, '%Y%m%d')
        today_date = datetime.datetime.today()
        day_gap = (today_date - insert_date).days

        batch_label = ''
        batch_label_chinese = ''
        if day_gap >= 7 :
            batch_label = 'v2'
            batch_label_chinese = '二次结佣'
        elif day_gap <= 3 :
            batch_label = 'v1'
            batch_label_chinese = '一次结佣'

        get_contents = dataframe['打款账户'][index]
        if type(get_contents) == type(1.00) :
            get_contents = int(get_contents)

        insert_date = datetime.datetime.strftime(insert_date, '%Y%m%d')
        insert_into_orderID = "A{a}_{b}{c}".format(a = insert_date, b = get_contents ,c = batch_label)
        dataframe['orderID(结算日期加营业员手机号)'][index] = insert_into_orderID

        if (dataframe['销售代表对应UID'][index]  is not np.nan) & (dataframe['商户对应UID'][index]  is  np.nan) == True:
            dataframe['打款支付宝账户'][index] = str(dataframe['user_info销售代表打款支付宝账户'][index])
            dataframe['打款支付宝认证'][index] = str(dataframe['user_info销售代表打款支付宝账户认证人'][index])
            dataframe['备注：结算对象'][index] = dataframe['合并销售代表名称'][index]
            dataframe['备注2：结算方式'][index] = '销售代表'
            dataframe['备注3：结佣批次'][index] = batch_label_chinese
            continue
        elif (dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is not np.nan) == True:
            dataframe['打款支付宝账户'][index] = str(dataframe['user_info商户支付宝'][index])
            dataframe['打款支付宝认证'][index] = str(dataframe['user_info商户支付宝账号认证人'][index])
            dataframe['备注：结算对象'][index] = dataframe['商户名称'][index]
            dataframe['备注2：结算方式'][index] = '商户'
            dataframe['备注3：结佣批次'][index] = batch_label_chinese
            continue
        elif (dataframe['销售代表对应UID'][index]  is not np.nan) & (dataframe['商户对应UID'][index]  is not np.nan) == True:
            dataframe['打款支付宝账户'][index] = str(dataframe['user_info商户支付宝'][index])
            dataframe['打款支付宝认证'][index] = str(dataframe['user_info商户支付宝账号认证人'][index])
            dataframe['备注：结算对象'][index] = dataframe['商户名称'][index]
            dataframe['备注2：结算方式'][index] = '商户'
            dataframe['备注3：结佣批次'][index] = batch_label_chinese
            continue
        elif ((dataframe['销售代表对应UID'][index]  is  np.nan) & (dataframe['商户对应UID'][index]  is np.nan) & (dataframe['打款账户'][index]  is not np.nan ) )== True :
            dataframe['打款支付宝账户'][index] = str(dataframe['营业员支付宝账户'][index])
            dataframe['打款支付宝认证'][index] = str(dataframe['营业员支付宝账户认证人'][index])
            dataframe['备注：结算对象'][index] = dataframe['营业员姓名'][index]
            dataframe['备注2：结算方式'][index] = '营业员'
            dataframe['备注3：结佣批次'][index] = batch_label_chinese
            continue
    return dataframe


def write_to_excel_a(dataframe,output_path):
    for index in range(len(dataframe)):
        dataframe.loc[index:index, ['营业员UID']] = str(dataframe.loc[index:index,['营业员UID']].values[0][0])
        dataframe.loc[index:index, ['商户UID']] =  str(dataframe.loc[index:index, ['商户UID']].values[0][0])
    dataframe.to_excel(output_path,encoding='utf-8',index=False,sheet_name=r'匹配明细')



def write_to_excel_c(dataframe,dict_path,output_path):
    date = datetime.datetime.now().strftime('%Y%m%d')
    with open(dict_path,encoding='utf-8') as f:
        dic_data = f.readlines()
        dic_data = [ele.split() for ele in dic_data]
    dic = {item[1]:item[0] for item in dic_data}
    dic_keys = list(dic.keys())
    dic_values = list(dic.values())
    dic_region = set(list(dic.values()))
    for region in dic_region:
        key_line = []
        for i, p in enumerate(dic_values):
            if p == region :
                key_line.append(dic_keys[i])
        df = dataframe[dataframe['区域编码'].isin(key_line)]
        if len(df) == 0:
            continue
        file_name = output_path + os.sep + '{}_手淘拉新返点明细表_{}.xlsx'.format(date,region)
        print(file_name)
        df.to_excel(file_name, encoding='utf-8', index=False)
        print('完成输出')


def empty_dataframe(shape,columns):
    data = np.zeros(shape)
    df = pd.DataFrame(data=data, columns=columns)
    for content in columns:
        df[content]=np.nan
    return df

def create_transfer_details(dataframe,pd_length):
    columns = [ 'activityID(固定值120)', 'orderID(结算日期加营业员手机号)', 'agentID', 'businessID', 'shopID', 'assistant',
               'areaCode',
               'moneyType(固定值1)', 'payAccount(营业员支付宝UID)', 'payAccountName', 'money(发好多钱)', 'status(固定值0)',
               'couponNO1',
               'couponNO2', 'couponNO3', 'couponNO4', 'couponNO5', 'remark(支付描述-日期-营业员手机号)', 'delflag', 'payNo', 'payTime', 'payDetail']
    col_length = len(columns)
    df = empty_dataframe([pd_length,col_length],columns)


    for i_index in range(pd_length):

        insert_date2 = str(dataframe['日期'][i_index])
        insert_date = datetime.datetime.strptime(insert_date2, '%Y%m%d')
        today_date = datetime.datetime.today()
        day_gap = (today_date - insert_date).days

        batch_label = ''
        batch_label_chinese = ''
        if day_gap >= 7:
            batch_label = 'v2'
            batch_label_chinese = '(二次结佣)'
        elif day_gap <= 3:
            batch_label = 'v1'
            batch_label_chinese = '(一次结佣)'


        get_contents = dataframe['打款账户'][i_index]
        insert_contents = "T{a}_{b}{c}".format(a = insert_date2 ,b = get_contents , c = batch_label)
        insert_contents_remark = '淘宝拉新奖励_{a}_{b}{c}'.format(a = insert_date2, b = dataframe['备注：结算对象'][i_index],
                                                             c = batch_label_chinese)
        df['orderID(结算日期加营业员手机号)'][i_index] =  insert_contents

        df['payAccount(营业员支付宝UID)'][i_index] = dataframe['打款UID'][i_index]
        df['money(发好多钱)'][i_index] = dataframe['佣金'][i_index]
        df['remark(支付描述-日期-营业员手机号)'][i_index] = insert_contents_remark
    df['activityID(固定值120)'] = 120
    df['moneyType(固定值1)'] = 1
    df['status(固定值0)'] = 0
    return df

def pivot_group_by(dataframe,output_path):
    pd_output = dataframe.fillna('$')
    cols =  pd_output.columns.values.tolist()
    cols.remove('money(发好多钱)')
    y = pd.pivot_table(pd_output,index=cols,values = ['money(发好多钱)'],aggfunc=np.sum)
    y.to_excel(output_path, sheet_name='佣金计算', encoding='utf-8', index=True, merge_cells=False)


if __name__ == '__main__':
    # -----paths-----
    date = datetime.datetime.now().strftime('%Y%m%d')                                       #获取操作当日日期
    # input_file_path = r'C:\Users\10854\Desktop\laxin\taoblx\input' # BY ylj
    # output_file_path = r'C:\Users\10854\Desktop\laxin\taoblx\output' # BY ylj
    input_file_path = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/taobao/input'    #输入文件主路径
    output_file_path = '/Users/Apple/Desktop/working/8 华院项目/运营自动化程序/taobao/output'  #输出文件主路径
    match_info = input_file_path + os.sep + 'match_info.xlsx'                               #math_info 表的路径和名称
    dict_path = input_file_path + os.sep + '区域划分.csv'                                    #区域划分表的路径和名称


    file_name = search_new_input_file(input_file_path)                                      #获取操作日日期的文件名
    detail = input_file_path + os.sep + '{}'.format(file_name)                              #操作文件完整路径

    pd_match_info_aim = read_match_info(match_info ,
                                        ['销售代表编码', '销售代表名称', '支付宝账号认证人', '营业员绑定支付宝', 'UID'])    #match_info要关联的字段，可以修改
    pd_detail = read_detail(detail)    #读取Excel表到pandas
    pd_detail = connection_with_match_info(pd_detail,pd_match_info_aim)         #把user_info表和原始表关联


    pd_detail = create_new_line(pd_detail,'打款账户')                            #新建列
    index1 = get_vacant_index(pd_detail,'商户对应UID')                           #获取对应字段空的行位置
    index2 = get_vacant_index(pd_detail,'销售代表对应UID')                        #获取对应字段空的行位置
    pd_detail = write_index_line(pd_detail,index1,'打款账户','商户支付宝账户')     #将非空行的数值传给'打款账户'
    pd_detail = write_index_line(pd_detail,index2,'打款账户','销售代表支付宝账户')  #将非空行的数值传给'打款账户'
    pd_detail = create_new_line(pd_detail,'打款UID')                             #新建列


    index3 = len(pd_detail)
    pd_detail = match_uid(pd_detail,index3)                                     #匹配三个角色的UID码

    pd_detail = create_new_line(pd_detail,'打款支付宝账户')                        #新建列
    pd_detail = create_new_line(pd_detail,'打款支付宝认证')                        #新建列
    pd_detail = create_new_line(pd_detail,'备注：结算对象')                        #新建列
    pd_detail = create_new_line(pd_detail, '备注2：结算方式')                      #新建列
    pd_detail = create_new_line(pd_detail, '备注3：结佣批次')                      #新建列
    pd_detail = create_new_line(pd_detail, 'orderID(结算日期加营业员手机号)')       #新建列

    pd_detail = remarks_supplements(pd_detail)                                   #备注以及补充内容关联
    pd_detail = create_new_line(pd_detail, '结算日期')                            #新建列
    pd_detail['结算日期'] = date                                                  #添加结算日期


    # 在此处输入DROP列的列名，删除不需要的列，添加列名
    pd_detail = pd_detail.drop(['user_info商户支付宝账号认证人','user_info商户支付宝','user_info销售代表打款支付宝账户认证人',
                                'user_info销售代表打款支付宝账户'], axis=1)

    output_a_table = output_file_path + os.sep + '手淘拉新返点明细表_{}.xlsx'.format(date)  # a表输出名称和路径
    write_to_excel_a(pd_detail,output_a_table)                                           #输出a表 《手淘拉新返点明细表》
    print('手淘拉新返点明细表_{}.xlsx  已生成'.format(date) )
    write_to_excel_c(pd_detail, dict_path, output_file_path)                             #输出各区域的《手淘拉新返点明细表》


    pd_output = create_transfer_details(pd_detail,pd_length=len(pd_detail))                 #生成《手淘拉新打款明细表》的关联
    output_b_table = output_file_path + os.sep + '手淘拉新打款明细表_{}.xlsx'.format(date)     #生成《手淘拉新打款明细表》的输出路径和文件名
    pivot_group_by(pd_output,output_b_table)                                                #输出《手淘拉新打款明细表》
    print('手淘拉新打款明细表_{}.xlsx  已生成'.format(date))
