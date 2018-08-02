
# coding=utf-8
"""
根据上一步骤得到的CSV文件，将搜索文本以及三个属性剥离，保存为相应的文件
注意路径
"""
import pandas as pd

#path of the train and test files
trainname = '/Volumes/d/data/sougoudata_ori/user_tag_query.10W.TRAIN.csv'
testname = '/Volumes/d/data/sougoudata_ori/user_tag_query.10W.TEST.csv'

root_path = '/Volumes/d/data/sougoudata_ori/'
data = pd.read_csv(trainname,encoding='gb18030')
print(data.info())

#generate three labels for age/gender/education
data.age.to_csv(root_path+"train_age.csv", index=False,encoding='gb18030')
data.Gender.to_csv(root_path+"train_gender.csv", index=False,encoding='gb18030')
data.Education.to_csv(root_path+"train_education.csv", index=False,encoding='gb18030')
#generate trainfile's text file
data.QueryList.to_csv(root_path+"train_querylist.csv", index=False,encoding='gb18030')

data = pd.read_csv(testname,encoding='gb18030')
print(data.info())
#generate testfile's text file
data.QueryList.to_csv(root_path+"test_querylist.csv", index=False,encoding='gb18030')
