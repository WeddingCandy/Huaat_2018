# -*- coding:UTF-8 -*
import  requests,sys
from bs4 import  BeautifulSoup
import pandas as pd
import encodings
import re
import time
import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

excel_sheet = pd.read_excel('C:/Users/thinkpad/Desktop/adx.xlsx',sheet_name = 'sheet1',header= 0)
# excel_sheet = pd.read_excel(r'/Users/Apple/Desktop/working/0 华院资料/HIVE库表/9 用户浏览标签 -20180319.xlsx',sheet_name = 'url',header= 0)
# excel_sheet_extract = excel_sheet.ix[excel_sheet['数据源类别\n1为网站\n2为APP']<2,['行业一级大类','行业二级大类', 'webname']].reset_index()
excel_sheet['label_contents'] = 'NULL'
# colums_aim = excel_sheet.ix[excel_sheet['数据源类别\n1为网站\n2为APP']<2 ,3:4].reset_index()
labels_ori = "http://" + excel_sheet.iloc[:,0:1]
labels = labels_ori.values.tolist()
count_failure = 0 ;count_success = 0
length = len(labels)
# length = 50
for id in range(0,length):
    try:
        req = requests.get(url=labels[id][0], headers=headers ,timeout=2)
        if req == None:
            continue
        else:
            html = req.text.encode(req.encoding).decode(req.encoding)
        # print('have read'+str(id+1))
    except Exception  as e:
        print("Exception: {}".format(e))
        count_failure += 1
        # print('第%d个label无法爬取,失败次数%d' %(id+1,count_failure) )

        continue
    else:
        data =req.json


    # html0 =req.content.decode('gbk', 'ignore')
    bf = BeautifulSoup(html, "html.parser")
    meta_all = bf.find_all('title')
    # meta_all = bf
    meta_tostring = str(meta_all)
    # string = '<meta content="保险，平安保险，车险，贷款，理财，信用卡，意外保险，重疾险，小额贷款，信用贷款，投资理财，个人理财，汽车保险，商业保险，少儿保险，健康保险，旅游保险，人寿保险, 医疗保险，平安普惠，平安信用卡，平安车险，平安银行" name="keywords">'
    meta_keyword = re.finditer(
        re.compile(r'([\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+){1,}'),
        meta_tostring)
    keep = []
    for i in meta_keyword:
        # print(i.group() + '\n')
        keep.append(i.group())
    keep = list(set(keep))
    count_success += 1
    print('第%s个label已完成，成功次数%d' %(id+1,count_success))

    excel_sheet.ix[id:id,'label_contents'] = str(keep).replace('[','').replace(']','')

time =str(time.time())
path = 'C:\\Users\\thinkpad\\Desktop\\result_adx_'+time+'.csv'
excel_sheet.to_csv(path,encoding='utf_8_sig' )
success_rate = float(count_success/(count_success+count_failure)*100)
print('成功数为：%d,成功率为：%f ' %(count_success,success_rate))

