# -*- coding:UTF-8 -*
"""
@author    Chans
@date    27/04/2018
@version description:
爬取“站长之家”行业分类 -"http://top.chinaz.com/hangye/"
"""

import os
import  requests
from bs4 import  BeautifulSoup
import pandas as pd
import re
import time
import random



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}


##调用目标网址,返回网址地址LIST 和 TAG
def get_target_website(filepath_in):
    with open(filepath_in,'r',encoding='utf-8') as f:
        contents = f.readlines()
        websites_and_catogories_list = []
        for line in contents:
            line_split = line.split()
            websites_and_catogories_list.append(line_split)
    return websites_and_catogories_list


##输出抓取后的信息到Excel
def ouput_crawler_result(filepath_output,pd_output,catogory):
    filename =  filepath_output + os.sep + catogory+'.xlsx'
    pd_output.to_excel(filename,sheet_name='results',encoding = 'utf-8')
    print('The file %s is done' %(filename))



##获取目标网址信息
def get_website_infos(catogory,target,page_num,dataframe):


    # user_agents = [
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    #     'mozilla/5.0 (windows nt 10.0; wow64) applewebkit/537.36 (khtml, like gecko) chrome/65.0.3325.181 safari/537.36',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 BIDUBrowser/6.x Safari/537.31',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.44 Safari/537.36 OPR/24.0.1558.25 (Edition Next)',
    #     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36 OPR/23.0.1522.60 (Edition Campaign 54)',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    # ]
    # user_agent = random.choice(user_agents)


    # data = {"catogory": ["生活服务", "娱乐休闲"], "website": ['jia.com', 'hexun.com'], "name": ["易车网", "58同城 "], "page_num": [1, 2]}
    # dataframe = pd.DataFrame(data,columns=["catogory", "website", "name" , "page_num"])
    req = requests.get(url=target,timeout=10,headers=headers) #    req = requests.get(url=target,timeout=10) #
    # website_content = req.content.decode('utf-8')
    bf = BeautifulSoup(req.content, "html.parser")
    info_judgement = bf.find_all('h2')
    try:
        # print(info_judgement[0])
        tip1 = '抱歉, 您所查找的页面不存在, 可能已被删除或您输错了网址!'
        tip2 = '404 Error'
        pattern1 = re.compile(tip1)
        pattern2 = re.compile(tip2)
        x1 = pattern1.findall(str(info_judgement))[0] #当没有错误信息返回时，info_judgement为空
        x2 = pattern2.findall(str(info_judgement))[0]
        print(x1)
        if x1 is not None or x2 is not None:
            # print(info_judgement[0].string )
            circle_info = 'end'
            return dataframe ,circle_info
    except Exception as e:
        print('pass')
    info = bf.find_all('a',attrs={'class':'pr10 fz14','target':'_blank'})
    pattern = re.compile('/site_([_\.a-zA-Z0-9/\?]+)\.html')
    for i , x in enumerate(info):
        name = x.string
        html = x.get('href')
        html_process =  pattern.findall(html)
        if len(html_process) > 0 :
            website = 'http://' + html_process[0]
            dataframe = dataframe.append(
                {"catogory": catogory, "website": website, "name": name, "page_num": page_num}, ignore_index=True)
        else:
            continue
    circle_info = 'start'
    return dataframe,circle_info

##主程序
def main_process(target_list):
    pattern_html = re.compile('([/:\.a-zA-Z0-9_]+).html')
    for line in target_list:
        if line[0] != 'end' :
            time.sleep(100)
            catogory = line[1]
            target = line[0]
            all_info = pd.DataFrame(columns=["catogory", "website", "name" , "page_num"])
            COUNT = 1
            tag = 'start'
            while tag != 'end':
                try:
                    if COUNT == 1:
                        print(target, COUNT)
                        all_info ,circle_info= get_website_infos(catogory,target,COUNT,all_info)
                        time.sleep(random.randint(3, 4))
                        COUNT += 1
                        tag = 'start'
                    elif COUNT > 1 :
                        target_1 = pattern_html.findall(target)[0] + '_' + str(COUNT) +'.html'
                        print(target_1,COUNT)
                        all_info,circle_info = get_website_infos(catogory,target_1,COUNT,all_info)
                        COUNT += 1
                        time.sleep(random.randint(15, 20))
                        if circle_info == 'end':
                            ouput_crawler_result(filepath_output, all_info, catogory)
                            tag = 'end'
                            break
                        tag = 'start'
                except Exception as e :
                    ouput_crawler_result(filepath_output, all_info, catogory)
                    print(e)
                    tag = 'end'
            continue
        else :
            break



# filepath_in = '/Volumes/d/huaat/huaat_crawlers/website_labels_supplement/target_website.txt' #in Mac
# filepath_output ='/Volumes/d/huaat/huaat_crawlers/website_labels_supplement/output' #in Mac

filepath_in = r'E:\huaat\huaat_crawlers\website_labels_supplement\target_website.txt'
filepath_output = r'E:\huaat\huaat_crawlers\website_labels_supplement\output'


websites_and_ccatogories_list = get_target_website(filepath_in)
main_process(websites_and_ccatogories_list)
# target = 'http://top.chinaz.com/hangye/index_shenghuo.html'
# catogory = '生活服务'







