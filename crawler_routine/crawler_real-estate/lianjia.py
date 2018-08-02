# -*- coding:utf-8 -*-
import os, re, time, random, urllib.request
####################
def openurl(url, head):
    match = re.search(r'^http[s]{0,}://.*', url)
    if match:
        url_tmp = url
    else:
        url_tmp = "http://" + url
    req = urllib.request.Request(url_tmp, headers=head, method='GET')
    response = urllib.request.urlopen(req)
    heads = response.getheaders()
    html = response.read()
    response.close()
    return html

def writeDictfile(filename, **dict):
    file = open(filename, 'w', encoding='utf-8')
    for i in dict:
        file.write(i + ":" + dict[i] + "\n")
    file.close()

def time_log(msg):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print(now + ":" + msg)

def readDictfile(filename):
    file = open(filename, "r")
    dict_t={}
    for i in file:
        m = re.split(r':', i , 1)
        dict_t[m[0]] = m[1].strip('\n')
    file.close()
    return dict_t

def sleepRandom(b = 5, e = 10, p = "TRUE"):
    t = random.randint(b, e)
    if p:
        time_log("app will sleep" + str(t) + "sec.")
    time.sleep(t)

####################
#print(os.getcwd())
os.chdir("C:/ttt")
#print(os.getcwd())
####################
data = readDictfile("all_house_tt.txt")

#des_path = "D:/python_test/URL"
des_path = "C:/ttt/output_1"

des_file_list = []
for fpathe, ddirs, ffs in os.walk(des_path):
    for ff in ffs:
        dmd = re.findall(r'output_(.*?).txt', ff)
        des_file_list.append(dmd[0])
print(des_file_list)

print("==================================")

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 BIDUBrowser/6.x Safari/537.31',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.44 Safari/537.36 OPR/24.0.1558.25 (Edition Next)',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36 OPR/23.0.1522.60 (Edition Campaign 54)'
]

for url in data:
    #print(url)
    #print(data[url])
    city = data[url]

    if city not in des_file_list:
        time_log("_____" + city + "____SSSSSSS")
        dict_next_page = {}
        next_url = url
        max_page = 0
        next_page = {}
        output = {}
        #print(url)
        output_1 = []
        error_output = {}

        user_agent = random.choice(user_agents)
        aheaders = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                     'Connection': 'keep-alive',
                     #'GET': next_url,
                     'User-Agent': user_agent
                    }
        html = openurl(url, aheaders)
        html = html.decode('utf-8')


        match_no = re.findall(r'没有找到相关内容', html)
        if len(match_no) > 0:
            no = match_no[0]
            print(no)
        else:
            # 頁數
            match_max_page = re.findall(r'"totalPage":(.*?),"curPage"', html)
            if len(match_max_page) > 0:
                max_page = match_max_page[0]
            else:
                max_page = 1
            print(max_page)
            page = int(max_page)

            while page != 0:
                sleepRandom(2,3)
                if(page==1):
                    next_url = url
                else:
                    next_url = url + "/pg" + str(page) + "/"
                #print(next_url)
                #print(page)

                user_agent = random.choice(user_agents)
                aheaders = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                             'Connection': 'keep-alive',
                             #'GET': next_url,
                             'User-Agent': user_agent
                            }
                try:
                    html = openurl(next_url, aheaders)
                    html = html.decode('utf-8')

                    part = r'<div class="title"><a href="(.*?)" target="_blank" data-bl="list"'
                    matchs = re.findall(part, html, re.S | re.M)
                    if len(matchs) == 0:
                        part = r'<h2><a target="_blank" href="(.*?)" data-el="ershoufang" title='
                        matchs = re.findall(part, html, re.S | re.M)
                    #print(matchs)

                    for match in matchs:
                        sleepRandom(2, 4)
                        url_tmp =   match
                        print(url_tmp)
                        user_agent = random.choice(user_agents)
                        aheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                    'Connection': 'keep-alive',
                                    # 'GET': next_url,
                                    'User-Agent': user_agent
                                    }
                        try:
                            next_html = openurl(url_tmp, aheaders)
                            next_html = next_html.decode('utf-8')

                            code=""
                            code_part = r'ershoufang/(.*?).html'
                            code_matchs = re.findall(code_part, match, re.S | re.M)
                            if len(code_matchs) > 0:
                                code = code_matchs[0]
                            #print(code)

                            title=""
                            title_part = r'<title>(.*?)</title>'
                            title_matchs = re.findall(title_part, next_html, re.S | re.M)
                            if len(title_matchs) > 0:
                                title = title_matchs[0]
                            #print(title)

                            price=""
                            price_part = r'<span class="total">(.*?)</span>'
                            price_matchs = re.findall(price_part, next_html, re.S | re.M)
                            if len(price_matchs) > 0:
                                price = price_matchs[0]
                            else:
                                price_part = r'售价：</dt><dd><span class="em-text"><strong class="ft-num">(.*?)</strong><span class="sub-text">万'
                                price_matchs = re.findall(price_part, next_html, re.S | re.M)
                                if len(price_matchs) > 0:
                                    price = price_matchs[0]
                            #print(price)

                            unitprice=""
                            unitprice_part = r'<span class="unitPriceValue">(.*?)<i>元/平米</i></span>'
                            unitprice_matchs = re.findall(unitprice_part, next_html, re.S | re.M)
                            if len(unitprice_matchs) > 0:
                                unitprice = unitprice_matchs[0]
                            else:
                                unitprice_part = r'单价：</dt><dd class="short">(.*?) 元/平米</dd></dl><dl>'
                                unitprice_matchs = re.findall(unitprice_part, next_html, re.S | re.M)
                                if len(unitprice_matchs) > 0:
                                    unitprice = unitprice_matchs[0]
                            #print(unitprice)

                            downpay=""
                            downpay_part = r'<div class="tax"><span>首付(.*?)万 </span>'
                            downpay_matchs = re.findall(downpay_part, next_html, re.S | re.M)
                            if len(downpay_matchs) > 0:
                                downpay = downpay_matchs[0]
                            else:
                                downpay_part = r'首付：</dt><dd class="short">(.*?) 万</dd></dl><dl><dt>'
                                downpay_matchs = re.findall(downpay_part, next_html, re.S | re.M)
                                if len(downpay_matchs) > 0:
                                    downpay = downpay_matchs[0]
                            #print(downpay)

                            monpay=""
                            monpay_part = r'月供：</dt><dd class="short">(.*?) 元</dd></dl><dl><dt>户型'
                            monpay_matchs = re.findall(monpay_part, next_html, re.S | re.M)
                            if len(monpay_matchs) > 0:
                                monpay = monpay_matchs[0]
                            #print(monpay)

                            design=""
                            design_part = r'<div class="room">\n        <div class="mainInfo">(.*?)</div>\n'
                            design_matchs = re.findall(design_part, next_html, re.S | re.M)
                            if len(design_matchs) > 0:
                                design = design_matchs[0]
                            else:
                                design_part = r'户型：</dt><dd>(.*?)</dd></dl><dl><dt>朝向'
                                design_matchs = re.findall(design_part, next_html, re.S | re.M)
                                if len(design_matchs) > 0:
                                    design = design_matchs[0]
                            #print(design)

                            area=""
                            area_part = r'<div class="area">\n        <div class="mainInfo">(.*?)平米</div>\n'
                            area_matchs = re.findall(area_part, next_html, re.S | re.M)
                            if len(area_matchs) > 0:
                                area = area_matchs[0]
                            else:
                                area_part = r'万</span><i>/ (.*?)㎡</i></span></dd></dl><dl><dt>'
                                area_matchs = re.findall(area_part, next_html, re.S | re.M)
                                if len(area_matchs) > 0:
                                    area = area_matchs[0]
                            #print(area)

                            floor=""
                            floor_part = r'所在楼层</span>(.*?)</li>'
                            floor_matchs = re.findall(floor_part, next_html, re.S | re.M)
                            if len(floor_matchs) > 0:
                                floor = floor_matchs[0]
                            else:
                                floor_part = r'楼层：</dt><dd>(.*?)</dd></dl><dl class="clear"><dt>'
                                floor_matchs = re.findall(floor_part, next_html, re.S | re.M)
                                if len(floor_matchs) > 0:
                                    floor = floor_matchs[0]
                            #print(floor)

                            orientations=""
                            orientations_part = r'房屋朝向</span>(.*?)</li>'
                            orientations_matchs = re.findall(orientations_part, next_html, re.S | re.M)
                            if len(orientations_matchs) > 0:
                                orientations = orientations_matchs[0]
                            else:
                                orientations_part = r'朝向：</dt><dd>(.*?)</dd></dl><dl><dt>楼层'
                                orientations_matchs = re.findall(orientations_part, next_html, re.S | re.M)
                                if len(orientations_matchs) > 0:
                                    orientations = orientations_matchs[0]
                            #print(orientations)

                            decoration=""
                            decoration_part = r'装修情况</span>(.*?)</li>'
                            decoration_matchs = re.findall(decoration_part, next_html, re.S | re.M)
                            if len(decoration_matchs) > 0:
                                decoration = decoration_matchs[0]
                            #print(decoration)

                            age=""
                            age_part = r'<div class="area">\n        <div class="mainInfo">(.*?)平米</div>\n                <div class="subInfo">(.*?)年建/(.*?)</div>'
                            age_matchs = re.findall(age_part, next_html, re.S | re.M)
                            if len(age_matchs) > 0:
                                age = age_matchs[0][1]
                            else:
                                age_part = r'data-el="bizcircle"(.*?)</span>(.*?)年</dd></dl></div>'
                                age_matchs = re.findall(age_part, next_html, re.S | re.M)
                                if len(age_matchs) > 0:
                                    age = age_matchs[0][1]
                            #print(age)

                            type=""
                            type_part = r'建筑类型</span>(.*?)</li>'
                            type_matchs = re.findall(type_part, next_html, re.S | re.M)
                            if len(type_matchs) > 0:
                                type = type_matchs[0]
                            #print(type)

                            village=""
                            village_part = r'<span class="label">小区名称</span>\n        <a href="(.*?)" target="_blank" class="info">(.*?)</a>'
                            village_matchs = re.findall(village_part, next_html, re.S | re.M)
                            if len(village_matchs) > 0:
                                village = village_matchs[0][1]
                            else:
                                village_part = r'小区：</dt><dd><a class="zone-name laisuzhou" data-bl="area" data-el="community" href="(.*?)">(.*?)</a><span class="region">'
                                village_matchs = re.findall(village_part, next_html, re.S | re.M)
                                if len(village_matchs) > 0:
                                    village = village_matchs[0][1]
                            #print(village)

                            address = ""
                            address_part = r'所在区域</span>\n        <span class="info"><a href="(.*?)" target="_blank">(.*?)</a>&nbsp;<a href="(.*?)" target="_blank">(.*?)</a>&nbsp;</span>'
                            address_matchs = re.findall(address_part, next_html, re.S | re.M)
                            if len(address_matchs) > 0:
                                address = address_matchs[0][1] + " " + address_matchs[0][3]
                            #print(address)

                            keyword = ""
                            keyword_part = r'<a class="tag" href="(\S+)">(\S+)</a>'
                            keyword_matchs = re.findall(keyword_part, next_html, re.S | re.M)
                            if len(keyword_matchs) > 0:
                                for uu in keyword_matchs:
                                    if len(keyword) > 0:
                                        keyword = uu[1] + "," + keyword
                                    else:
                                        keyword = uu[1]
                            else:
                                keyword_part = r'<div class="view-label">(.*?)<!-- 房屋信息区域，相册、详情、经纪人模块 -->'
                                keyword_matchs = re.findall(keyword_part, next_html, re.S | re.M)
                                if len(keyword_matchs) > 0:
                                    keyword_matchs = re.findall(r'<span>(\S+)</span></span>', keyword_matchs[0], re.S | re.M)
                                    for ee in keyword_matchs:
                                        if len(keyword)>0:
                                            keyword = ee + "," + keyword
                                        else:
                                            keyword = ee
                            #print(keyword)

                            output_1.append("3" + '\t' + "lianjia" + '\t' + city + '\t' + code + '\t' + title + '\t' + price + '\t' + unitprice + '\t' + downpay + '\t' + monpay + '\t' + design + '\t' + area + '\t' + age + '\t' + orientations + '\t' + floor + '\t' + decoration + '\t' + type + '\t' + village + '\t' + address + '\t' + keyword)
                            print(output_1)
                        except:
                            error_output[next_url] = url_tmp
                            print("NNNNNNNNNnn")
                except:
                    error_output[next_url] = url_tmp
                    print("NNNNNNNNNnn")
                    # output[url_tmp[7:]] ="3"+'\t'+"lianjia"+'\tcity='+city+'\tcode='+code+'\ttitle='+title+'\tprice='+price+'\tunitprice='+unitprice+'\tdownpay='+downpay+'\tmonpay='+monpay+'\tdesign='+design+'\tarea='+area+'\tage='+age+'\torientations='+orientations+'\tfloor='+floor+'\tdecoration='+decoration+'\ttype='+type+'\tvillage='+village+'\taddress='+address
                    # print(output)
                page = page - 1
            if len(error_output) > 0:
                writeDictfile("output_error/output_%s.txt" % city, **error_output)
            #writeDictfile("output/output_%s.txt" % city, **output)
            file = open("output_1/output_%s.txt" % city, 'w', encoding='utf-8')
            for i in output_1:
                file.writelines(i + "\n")
            file.close()
            time_log("__"+ city +"__"+ "EEEEEEEEE_End")
            print("@@@@@@@@@@@@@@@@@@@@@@@")