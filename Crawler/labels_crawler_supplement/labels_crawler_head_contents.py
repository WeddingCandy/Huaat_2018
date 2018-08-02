#Version 1.0
#@author Chans
# -*- coding:UTF-8 -*
import  requests,sys
from bs4 import  BeautifulSoup
import pandas as pd
import encodings
import re
import os


def get_contens_info(excel_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    excel_sheet = pd.read_excel(excel_name,sheet_name = 'results',header= 0)
    excel_sheet['label_contents'] = 'NULL'
    labels = excel_sheet['website'].values.tolist()
    count_failure = 0 ;count_success = 0
    length = len(labels)
    # length = 50
    for id in range(0,length):
        try:
            req = requests.get(url=labels[id], headers=headers ,timeout=10)
            if req == None:
                print('None')
                continue
            else:
                # print(req.encoding)
                # html = req.text.encode(req.encoding).decode(req.encoding)
                html = req.content
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
        meta_all = bf.find_all('head')
        # meta_all = bf
        meta_tostring = str(meta_all)
        # string = '<meta content="保险，平安保险，车险，贷款，理财，信用卡，意外保险，重疾险，小额贷款，信用贷款，投资理财，个人理财，汽车保险，商业保险，少儿保险，健康保险，旅游保险，人寿保险, 医疗保险，平安普惠，平安信用卡，平安车险，平安银行" name="keywords">'
        meta_keyword = re.finditer(
            re.compile(r'([\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+){1,}'),
            meta_tostring)
        keep = []
        for i in meta_keyword:
            keep.append(i.group())
        keep = list(set(keep))
        count_success += 1
        print('第%s个label已完成，成功次数%d' %(id+1,count_success))
        excel_sheet.loc[id:id,'label_contents'] = str(keep).replace('[','').replace("'",'').replace(']','')
    return excel_sheet

def pd_to_excel(pd_aim,excel_name_output):
    pd_aim.to_excel(excel_name_output,encoding='utf-8')
    print('o')


target_file = r'E:\huaat\huaat_crawlers\website_labels_supplement\output'
output_path = r'E:\huaat\huaat_crawlers\website_labels_supplement\output\gotten'
for root, dirs, files  in os.walk(target_file) :
    for file in files:
        excel_name = root+os.sep+file
        pd_aim = get_contens_info(excel_name)
        excel_name_output = output_path+os.sep+file
        pd_output = pd_to_excel(pd_aim,excel_name_output)



