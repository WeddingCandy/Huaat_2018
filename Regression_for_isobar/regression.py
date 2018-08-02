##!/usr/bin/python
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
index = []
x = np.arange(0,180,1).tolist()
for i in x:
    ''.join(str(i))

data = pd.read_excel(r'/Users/Apple/Desktop/working/1 isobar/药品/关键词TOP.xlsx',sheetname='keyword2总人数',
                     index =[  ] )

y = map(str,x)
columns_name = list(data.columns)
data[columns_name] = data[columns_name].apply(pd.to_numeric, errors ='ignore')
data.dtypes
data1 = data.loc[data['if_equal'] >0, columns_name[0:3]]
data2 = data.loc[((data['if_equal'] >0)&(data['匹配数量']<160000)), columns_name[0:3]]
print(len(data1),len(data2))
data_test = data.loc[data['if_equal'] ==0, columns_name[0:3]]

x_train_1 = data1['SUM']
x_validation = x_train_1.loc[['124'] , :]#124,129,133,137,165
x_train_2 = x_train_1 /(x_train_1.max()-x_train_1.min())
x_train_3 = data2['SUM']

y_train_1 = data1['匹配数量']
y_train_2 = data2['匹配数量']
x_test = data_test['SUM']
x_test1 = x_test/(x_test.max()-x_test.min())

lr = LinearRegression()
alpha_can = np.logspace(-3, 2, 10)  # 参数范围
np.set_printoptions(suppress=True)
model_lr3 = GridSearchCV(lr, param_grid={'alpha': alpha_can}, cv=2)  # cv折数，model模型，param_grid参数范围
model_lr1 = Pipeline([#('sc',StandardScaler() ),
                     ('lr',lr )])
model_lr2 = Pipeline([#('sc',StandardScaler() ),
                     ('lr',lr )])
model_lr4 = Pipeline([#('sc',StandardScaler() ),
                     ('lr',lr )])
model_lr1.fit(x_train_1.reshape(-1,1),y_train_1.reshape(-1,1)) #当x只有一列的时候，用reshape(-1,1)
model_lr2.fit(x_train_2.reshape(-1,1),y_train_1.reshape(-1,1)) #当x只有一列的时候，用reshape(-1,1)
model_lr4.fit(x_train_3.reshape(-1,1),y_train_2.reshape(-1,1))
# model_lr3.fit(x_train.reshape(-1,1),y_train.reshape(-1,1))
# order = x_test.argsort(axis=0)  # 输出顺序的索引
# x_test = x_test.values[order]
y_hat1 = model_lr1.predict(x_test.reshape(-1,1))
y_hat2 = model_lr2.predict(x_test1.reshape(-1,1))
y_hat4 = model_lr4.predict(x_test.reshape(-1,1))

print(type(y_hat1))
# y_hat3 = model_lr3.predict(x_test.reshape(-1,1))
data_test['y_hat1'] =pd.DataFrame(y_hat1,columns=['y_hat1'])
data_test['y_hat2'] =pd.DataFrame(y_hat2,columns=['y_hat2'])
data_test['y_hat4'] =pd.DataFrame(y_hat4,columns=['y_hat4'])
# data_test.to_excel(r'/Users/Apple/Desktop/result1.xlsx')
#画图
plt.figure(facecolor='w',figsize=(6,8))
t=np.arange(len(x_test))
plt.subplot(311)
plt.plot(t,y_hat1,'r-', linewidth=2, label='y_hat1')
plt.subplot(312)
plt.plot(t,y_hat2,'b-', linewidth=2, label='y_hat2')
# plt.subplot(313)
# plt.plot(t,y_hat3,'g-', linewidth=2, label='y_hat3')
plt.grid(b =True ,ls =':')
plt.show()
