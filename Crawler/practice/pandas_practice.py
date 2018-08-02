# -*- coding:UTF-8 -*

import  pandas as pd
aa = pd.read_csv('C:/Users/thinkpad/Desktop/result.csv')
a1= aa.iloc[:,2:]
a1.sort_values(by=['行业一级大类', '行业二级大类', 'webname'],ascending=[0,0,0],inplace=True)
# length= len(a1)
length = 100

for i in range(0,length):
    if (a1.iloc[i:i+1,0:0] == a1.iloc[i+1:i+2,0:0])&(a1.iloc[i:i+1,1:1] == a1.iloc[i+1:i+2,1:1]):
        print(a1[i])