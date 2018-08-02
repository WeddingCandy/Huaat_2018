# -*- coding: utf-8 -*-
"""
@CREATETIME: 20/07/2018 18:13 
@AUTHOR: Chans
@VERSION: 
"""


list_sony = ["索尼(SONY)KD-55X9000E 55英寸电视 4K超高清 安卓7.0智能电视 强劲芯片 索尼真品质 【客厅精选】",
"索尼(SONY)KD-65X7500F 65英寸 4K超高清 HDR智能电视 纤巧窄边框 安卓7.0",
"索尼(SONY)KD-65X9000F 65英寸 4K超高清 明锐动态技术让运动画面更清晰 安卓7.0让电视更智能",
"索尼(SONY)KD-65X8566F 65英寸 4KHDR技术与4K迅锐技术 让画面更清晰 安卓7.0让电视更智能",
"索尼(SONY)KD-55X7500F 55英寸 4K液晶智能电视 纤巧窄边框 丰富影视资源",
"索尼(SONY)KD-55X9000F 55英寸 4K超高清 明锐动态技术 让运动画面更清晰 安卓7.0让电视更智能",
"索尼(SONY)KD-49X7500F 49英寸 4K液晶 HDR智能电视 纤巧窄边框",
"索尼(SONY)KD-55X8566F 55英寸 4K HDR技术与4K迅锐技术 让画面更清晰 安卓7.0让电视更智能",
"索尼(SONY)KDL-50W660F 50英寸 全高清LED液晶电视 迅锐图像处理引擎画面更清晰",
"索尼(SONY)KD-55X8500F 55英寸 4KHDR技术与迅锐技术 画面更清晰 安卓7.0电视更智能",
"索尼(SONY)KD-43X8500F 43英寸 4K超高清 HDR智能电视 特丽魅彩 色彩更丰富",
"索尼(SONY)KD-49X8500F 49英寸 4K超高清 HDR液晶智能电视 安卓7.0",
"索尼（SONY）电视 KD-65X8566F 65英寸 大屏4K超高清 智能液晶平板电视 腾讯视频内容（黑色）",
"索尼（SONY）电视 KD-65X9000F 65英寸 大屏4K超清 智能液晶平板电视 精锐光控Pro增强版（黑色）",
"索尼（SONY）电视 KD-55X8566F 55英寸 4K超高清 智能网络液晶平板电视 腾讯视频内容（黑色）",
"索尼（SONY）电视 KD-55X9000F 55英寸 4K超高清 智能液晶平板电视 精锐光控Pro增强版（黑色）",
"索尼（SONY）KD-65X7500F 65英寸 4K HDR 智能网络 液晶电视 腾讯视频（黑色）",
"索尼（SONY）KD-55X7500F 55英寸 4K HDR 智能网络 液晶电视 腾讯视频（黑色）",
"索尼（SONY）KD-49X7500F 49英寸 4K HDR 智能网络 液晶电视 腾讯视频（黑色）",
"索尼（SONY）电视 KD-75X8566E 75英寸 大屏4K超高清 智能液晶平板电视机 特丽魅彩 HDR（黑色）",
"索尼（SONY）电视 KD-55X9000E 55英寸 4K超高清 智能液晶平板电视 精锐光控Pro HDR（银色）",
"索尼（SONY）KDL-50W660F 50英寸全高清液晶电视（黑色）",
"索尼（SONY）KD-65A8F 65英寸 OLED 4K HDR安卓7.0智能电视（黑色）",
"索尼（SONY）电视 KD-75X8500F 75英寸 大屏4K超高清 智能液晶平板电视 特丽魅彩 HDR（黑色）"]
list_sam = ["三星(SAMSUNG) UA55MUF30ZJXXZ 55英寸 4K超高清 网络智能 LED液晶平板电视 纤窄边框",
"三星(SAMSUNG) UA65KUC30SJXXZ 65英寸 4K超高清 HDR功能 曲面 网络 智能 LED液晶电视",
"三星(SAMSUNG) UA55KUC31SJXXZ 55英寸 4K超高清 HDR功能 曲面 智能 LED液晶电视",
"三星(SAMSUNG) UA65KUF30EJXXZ 65英寸 4K超高清 HDR功能 网络智能 LED液晶电视",
"三星(SAMSUNG) UA65MUF30EJXXZ 65英寸 4K超高清 HDR功能 网络 智能 纤薄 LED液晶电视",
"三星(SAMSUNG) UA49NU7000JXXZ 49英寸 4K超高清 UHD画质增强引擎 智能电视",
"三星(SAMSUNG) UA55MUF30EJXXZ 55英寸 4K超高清 HDR功能 网络智能 LED液晶电视",
"三星(SAMSUNG) UA65MUF40SJXXZ 65英寸 4K超高清HDR 纤窄边款 超薄设计 智能 液晶平板电视",
"三星(SAMSUNG) UA55MU6310JXXZ 55英寸 4K超高清 HDR功能 网络 智能 LED液晶电视",
"三星(SAMSUNG) QA65Q6FAMJXXZ 65英寸 超高清光质量子点QLED超薄 3边无边框 智能电视",
"三星(SAMSUNG) QA55Q6FAMJXXZ 55英寸 超高清光质量子点QLED超薄 3边无边框 智能电视",
"三星(SAMSUNG) UA65MU6990JXXZ 百年国米专属定制 4K超高清 HDR 曲面 智能 LED液晶电视",
"三星（SAMSUNG）UA55MUF30ZJXXZ 55英寸 4K超高清 智能网络 液晶平板电视 黑色",
"三星（SAMSUNG）UA65MUC30SJXXZ 65英寸 曲面 HDR 4K超高清 智能网络液晶电视 黑色",
"三星（SAMSUNG）UA55MUC30SJXXZ 55英寸 曲面 HDR 4K超高清 智能网络液晶电视 黑色",
"三星（SAMSUNG）UA49NU7000JXXZ 49英寸 UHD4K超高清 三面超窄边框 智能液晶电视 49NU7000天灰色",
"三星（SAMSUNG）UA55MUF30EJXXZ 55英寸 HDR UHD 4K超高清 智能网络 平板液晶电视 黑色",
"三星（SAMSUNG） UA65KUF30EJXXZ 65英寸4K液晶LED智能平板电视机 官方正品",
"三星（SAMSUNG）UA55MUF70AJXXZ 55英寸70A AI人工智能电视机 HDR 智能语音京东微联物联液晶电视 银色",
"三星（SAMSUNG） UA65KUC30SJXXZ 65英寸4K超清智能曲面HDR电视机 官方正品",
"三星（SAMSUNG） UA55KUC31SJXXZ 55英寸4K超高清智能曲面液晶电视 官方正品",
"三星（SAMSUNG） UA40KUF30EJXXZ 40英寸4K超高清智能网络HDR平板液晶电视机",
"三星（SAMSUNG）UA65NU7300JXXZ 65英寸 曲面UHD4K超高清 HDR 纤窄边框 智能液晶电视 65NU7300银色",
"三星（SAMSUNG） UA75MU6320JXXZ 75英寸4K超高清 HDR 智能液晶平板电视"]
list_mi = ["小米（MI）小米电视4A 32英寸L32M5-AZ 智能高清网络液晶平板电视机彩电 40",
"小米（MI）小米电视4A 55英寸L55M5-AZ/AD 4K超高清HDR 智能wifi网络液晶平板电视机",
"小米（MI）小米电视4A 49英寸L49M5-AZ 全高清1080P智能HDR wifi网络液晶平板电视机 50",
"小米（MI）小米电视4A 43英寸青春版L43M5-AD 全高清1080P 人工智能语音 网络平板液晶电视 带语音遥控器",
"小米（MI）小米电视4A 65英寸L65M5-AD 4K超高清HDR 智能语音 wifi网络液晶平板电视机60/70",
"小米（MI）小米电视4C 43英寸L43M5-AX 智能全高清1080P大存储 wifi网络智能平板液晶电视机",
"小米(MI) 小米电视4 55英寸L55M5-AB 超薄4K超高清HDR 人工智能语音 智能网络液晶平板电视",
"小米（MI）小米电视4C 55英寸L55M5-AZ 4K超高清HDR 智能wifi语音彩电 网络液晶平板电视机",
"小米（MI）小米电视4C 55英寸体育版L55M5-AZ 4K超高清HDR 人工智能 PPTV定制 网络液晶平板电视机",
"小米（MI）小米电视4A 65英寸 4k超高清HDR wifi网络智能液晶平板电视机 55 70彩电",
"小米（MI）小米电视4A PPTV定制版 L43M5-AZ 43英寸 体育版HDR全高清1080P安卓智能液晶平板电视机",
"小米（MI）小米电视4X 55英寸L55M5-AD 4K超高清HDR 人工智能语音 蓝牙网络液晶平板电视机",
"小米（MI）小米电视4A 55英寸 L55M5-AZ/L55M5-AD 2GB+8GB HDR 4K超高清 人工智能网络液晶平板电视",
"小米（MI）小米电视4A 32英寸 L32M5-AZ 1GB+4GB 四核处理器 高清人工智能网络液晶平板电视",
"小米（MI）小米电视4S 50英寸 L50M5-AD 2GB+8GB 4K超高清 蓝牙语音遥控 人工智能语音网络液晶平板电视",
"小米（MI）小米电视4C 50英寸 L50M5-AD 2GB+8GB HDR 4K超高清 蓝牙语音遥控 人工智能语音网络液晶平板电视",
"小米（MI）小米电视4A 50英寸 L50M5-AD 2GB+8GB HDR 4K超高清 蓝牙语音遥控 人工智能语音网络液晶平板电视",
"小米（MI）小米电视4A 65英寸 L65M5-AZ/L65M5-AD 2GB+8GB HDR 4K超高清 人工智能网络液晶平板电视",
"小米（MI）小米电视4A 40英寸 L40M5-AD 1GB+8GB 全高清 蓝牙语音遥控 人工智能语音网络液晶平板电视",
"小米（MI）小米电视4A 43英寸 青春版 L43M5-AD 1GB+8GB 全高清 蓝牙语音遥控 人工智能语音网络液晶平板电视",
"小米（MI）小米电视4 55英寸 L55M5-AB 4.9mm超薄 2GB+8GB HDR 4K超高清 蓝牙语音 人工智能语音平板电视",
"小米（MI）小米电视4C 55英寸 L55M5-AZ 2GB+8GB HDR 4K超高清 人工智能网络液晶平板电视",
"小米（MI）小米电视4C 43英寸 L43M5-AX 1GB+8GB 全高清 人工智能网络液晶平板电视",
"小米（MI）小米电视4S 55英寸 L55M5-AD 2GB+8GB HDR 4K超高清 蓝牙语音遥控 人工智能语音网络液晶平板电视"]

len_sony = len(list_sony)
len_sam = len(list_sam)
len_mi = len(list_mi)


list_sony_mi = []
list_sony_sam = []
for i in range(len_sony):
    for t in range(len_mi):
        list_sony_mi.append(list_sony[i]+':'+list_mi[t])
# print(list_sony_mi)

for i in range(len_sony):
    for t in range(len_sam):
        list_sony_sam.append(list_sony[i]+':'+list_sam[t])
print(list_sony_sam)
