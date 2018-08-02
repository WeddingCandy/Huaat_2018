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
    'mozilla\/5.0 (windows nt 10.0; wow64) applewebkit/537.36 (khtml, like gecko) chrome/65.0.3325.181 safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 BIDUBrowser/6.x Safari/537.31',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.44 Safari/537.36 OPR/24.0.1558.25 (Edition Next)',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36 OPR/23.0.1522.60 (Edition Campaign 54)'
]
village=""
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
        output_1 = []
        error_output = {}

        while next_url != "NO":
            sleepRandom(2,3)
            print(next_url)
            cc_part = r'(.*?)/ershoufang/'
            cc_matchs = re.findall(cc_part, next_url, re.S | re.M)
            if len(cc_matchs) > 0:
                cc = cc_matchs[0]

            user_agent = random.choice(user_agents)
            aheaders = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                         'Connection': 'keep-alive',
                         #'GET': next_url,
                         'User-Agent': user_agent
                        }
            try:
                html = openurl(next_url, aheaders)
                html = html.decode('utf-8')
                #print(html)

                part = r'<p class="bthead">\t\r\n {1,}\t<a href="(.*?)"'
                matchs = re.findall(part, html, re.S | re.M)
                if matchs:
                    print(matchs)
                else:
                    part = r'<p class="bthead">\r\n {1,}<a href="(.*?)"'
                    matchs = re.findall(part, html, re.S | re.M)
                #matchs = matchs[0:1]

                for match in matchs:
                    sleepRandom(1, 2)
                    url_tmp =  match
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
                        code_part = r'/ershoufang/(.*?)x.shtml'
                        code_matchs = re.findall(code_part, match, re.S | re.M)
                        if len(code_matchs) > 0:
                            code = code_matchs[0]
                        else:
                            code_part = r'entinfo=(.*?)_0'
                            code_matchs = re.findall(code_part, match, re.S | re.M)
                            if len(code_matchs) > 0:
                                code = code_matchs[0]
                        print(code)

                        title=""
                        title_part = r'<title>(.*?)\r\n</title>'
                        title_matchs = re.findall(title_part, next_html, re.S | re.M)
                        if len(title_matchs) > 0:
                            title = title_matchs[0]
                        else:
                            title_part = r'<title>(.*?)</title>'
                            title_matchs = re.findall(title_part, next_html, re.S | re.M)
                            if len(title_matchs) > 0:
                                title = title_matchs[0]
                        print(title)

                        price=""
                        price_part = r'售价：(.*?)万元'
                        price_matchs = re.findall(price_part, next_html, re.S | re.M)
                        if len(price_matchs) > 0:
                            price = price_matchs[0]
                        print(price)

                        unitprice=""
                        unitprice_part = r'万元（(.*?)元/㎡）；'
                        unitprice_matchs = re.findall(unitprice_part, next_html, re.S | re.M)
                        if len(unitprice_matchs) > 0:
                            unitprice = unitprice_matchs[0]
                        print(unitprice)

                        downpay=""
                        downpay_part = r'<span class="mr5">首付约(.*?)万</span>'
                        downpay_matchs = re.findall(downpay_part, next_html, re.S | re.M)
                        if len(downpay_matchs) > 0:
                            downpay = downpay_matchs[0]
                        else:
                            downpay_part = r'房贷：首付约(.*?)万'
                            downpay_matchs = re.findall(downpay_part, next_html, re.S | re.M)
                            if len(downpay_matchs) > 0:
                                downpay = downpay_matchs[0]
                        print(downpay)

                        monpay=""
                        monpay_part = r'<span class="mr5">月供约(.*?)元</span>'
                        monpay_matchs = re.findall(monpay_part, next_html, re.S | re.M)
                        if len(monpay_matchs) > 0:
                            monpay = monpay_matchs[0]
                        else:
                            monpay_part = r'月供约（(.*?)）；'
                            monpay_matchs = re.findall(monpay_part, next_html, re.S | re.M)
                            if len(monpay_matchs) > 0:
                                monpay = monpay_matchs[0]
                        print(monpay)

                        design=""
                        design_part = r'户型：(.*?)卫(.*?)㎡；'
                        design_matchs = re.findall(design_part, next_html, re.S | re.M)
                        if len(design_matchs) > 0:
                            design = design_matchs[0][0] + "卫"
                        else:
                            design_part = r'户型：</div>\n {1,}<div class="su_con">\n {1,}(.*?)\n {1,}(.*?)\n {1,}(.*?)\n {1,}&nbsp;&nbsp;&nbsp;&nbsp'
                            design_matchs = re.findall(design_part, next_html, re.S | re.M)
                            if len(design_matchs) > 0:
                                #design = design_matchs[0]
                                for ee in design_matchs[0]:
                                    if len(design) > 0:
                                        design = ee + " " + design
                                    else:
                                        design = ee
                        print(design)

                        area=""

                        floor=""
                        floor_part = r'房屋楼层：</li>\r\n\t\t\t\t\t\t\t\t\t\t\t<li class="des_cols2">(.*?)</li>'
                        floor_matchs = re.findall(floor_part, next_html, re.S | re.M)
                        if len(floor_matchs) > 0:
                            floor = floor_matchs[0]
                        else:
                            floor_part = r'房屋楼层：</li>\n {1,}<li class="des_cols2">(.*?)</li>'
                            floor_matchs = re.findall(floor_part, next_html, re.S | re.M)
                            if len(floor_matchs) > 0:
                                floor = floor_matchs[0]
                        print(floor)

                        orientations=""
                        orientations_part = r'朝向：</li>\r\n\t\t\t\t\t\t\t\t\t\t\t<li class="des_cols2">(.*?)</li>\r\n\t\t\t\t\t\t\t\t\t\t'
                        orientations_matchs = re.findall(orientations_part, next_html, re.S | re.M)
                        if len(orientations_matchs) > 0:
                            orientations = orientations_matchs[0]
                        else:
                            orientations_part = r'朝向：</li>\n {1,}<li class="des_cols2">(.*?)</li>'
                            orientations_matchs = re.findall(orientations_part, next_html, re.S | re.M)
                            if len(orientations_matchs) > 0:
                                orientations = orientations_matchs[0]
                        print(orientations)

                        decoration=""
                        decoration_part = r'装修程度：</li>\r\n\t\t\t\t\t\t\t\t\t\t\t<li class="des_cols2">(.*?)\t\t\t\t\t\t\t\t\t\t\t&nbsp;&nbsp;&nbsp'
                        decoration_matchs = re.findall(decoration_part, next_html, re.S | re.M)
                        if len(decoration_matchs) > 0:
                            decoration = decoration_matchs[0]
                        else:
                            decoration_part = r'装修程度：</li>\n {1,}<li class="des_cols2">(.*?) {1,}&nbsp;&nbsp;&nbsp;&nbsp;'
                            decoration_matchs = re.findall(decoration_part, next_html, re.S | re.M)
                            if len(decoration_matchs) > 0:
                                decoration = decoration_matchs[0]
                        print(decoration)

                        age=""
                        age_part = r'建造年代：</li>\r\n\t\t\t\t\t\t\t\t\t\t\t<li class="des_cols2">(.*?)年</li>'
                        age_matchs = re.findall(age_part, next_html, re.S | re.M)
                        if len(age_matchs) > 0:
                            age = age_matchs[0]
                        else:
                            age_part = r'建造年代：</li>\n {1,}<li class="des_cols2">(.*?)</li>'
                            age_matchs = re.findall(age_part, next_html, re.S | re.M)
                            if len(age_matchs) > 0:
                                age = age_matchs[0]
                        print(age)

                        type=""
                        type_part = r'住宅类别：</li>\r\n\t\t\t\t\t\t\t\t\t\t\t<li class="des_cols2">(.*?)</li>'
                        type_matchs = re.findall(type_part, next_html, re.S | re.M)
                        if len(type_matchs) > 0:
                            type = type_matchs[0]
                        else:
                            type_part = r'住宅类别：</li>\n {1,}<li class="des_cols2">(.*?)</li>'
                            type_matchs = re.findall(type_part, next_html, re.S | re.M)
                            if len(type_matchs) > 0:
                                type = type_matchs[0]
                        print(type)

                        address = ""
                        address_part = r'地址：</div>\r\n\t\t {1,}<div class="su_con su_gbconwidth">\r\n\t\t {1,}(.*?)\r\n\t\t {1,}\t'
                        address_matchs = re.findall(address_part, next_html, re.S | re.M)
                        if len(address_matchs) > 0:
                            address = address_matchs[0]
                        else:
                            address_part = r'地址：</div>\n {1,}<div class="su_con su_gbconwidth">\n {1,}(.*?) {1,}<a id="jtdt1"'
                            address_matchs = re.findall(address_part, next_html, re.S | re.M)
                            if len(address_matchs) > 0:
                                address = address_matchs[0]
                            else:
                                address_part = r'地址：</div>\n {1,}<div class="su_con su_gbconwidth">\n {1,}(.*?) {1,}</div>'
                                address_matchs = re.findall(address_part, next_html, re.S | re.M)
                                if len(address_matchs) > 0:
                                    address = address_matchs[0]
                        print(address)

                        keyword=""
                        keyword_part = r'<span class="g_tagSon(\d+)">(\S+)</span>'
                        keyword_matchs = re.findall(keyword_part, next_html, re.S | re.M)
                        if len(keyword_matchs) > 0:
                            for ee in keyword_matchs:
                                if len(keyword) > 0:
                                    keyword = ee[1] + "," + keyword
                                else:
                                    keyword = ee[1]
                        else:
                            keyword_part1 = r'<div class="g_tag">\n {1,}(.*?)</div>\n {1,}<!-- 房源特色 end -->'
                            keyword_matchs1 = re.findall(keyword_part1, next_html, re.S | re.M)
                            #print(keyword_matchs1[0])
                            if len(keyword_matchs1) > 0:
                                keyword_part = r'">(.*?)</span>'
                                keyword_matchs = re.findall(keyword_part, keyword_matchs1[0], re.S | re.M)
                                #print(keyword_matchs)
                                for ee in keyword_matchs:
                                    if len(keyword) > 0:
                                        keyword = ee + "," + keyword
                                    else:
                                        keyword = ee
                        print(keyword)

                        # output[url_tmp[7:]] ="3"+'\t'+str(58)+'\tcity='+city+'\tcode='+code+'\ttitle='+title+'\tprice='+price+'\tunitprice='+unitprice+'\tdownpay='+downpay+'\tmonpay='+monpay+'\tdesign='+design+'\tarea='+area+'\tage='+age+'\torientations='+orientations+'\tfloor='+floor+'\tdecoration='+decoration+'\ttype='+type+'\tvillage='+village+'\taddress='+address
                        # print(len(output))
                        output_1.append("2" + '\t' + str(58) + '\t' + city + '\t' + code + '\t' + title + '\t' + price + '\t' + unitprice + '\t' + downpay + '\t' + monpay + '\t' + design + '\t' + area + '\t' + age + '\t' + orientations + '\t' + floor + '\t' + decoration + '\t' + type + '\t' + village + '\t' + address + '\t' + keyword)
                        print(output_1)
                    except:
                        error_output[next_url]=url_tmp
                        print(error_output)
            except:
                error_output[next_url] = url_tmp
                #print(error_output)
            part_next_page = r'<a {1,}class="next" href="(\S+)"><span>下一页'
            next_match = re.findall(part_next_page, html, re.S | re.M)
            print(next_match)
            if len(next_match) > 0:
                next_url = next_match[0]
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print(next_url)
            else:
                next_url="NO"
        if len(error_output) > 0:
           writeDictfile("output_error/output_%s.txt" % city, **error_output)
        #writeDictfile("output/output_%s.txt" % city, **output)
        file = open("output_1/output_%s.txt" % city, 'w', encoding='utf-8')
        for i in output_1:
            file.writelines(i + "\n")
        file.close()
        #writeDictfile("output/output_%s.txt" % city, **output)
        time_log("__"+ city +"__"+ "EEEEEEEEE_End")
        print("@@@@@@@@@@@@@@@@@@@@@@@")