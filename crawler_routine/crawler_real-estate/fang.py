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
des_path = "C:/ttt/output"

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
downpay=""
monpay=""
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

        user_agent = random.choice(user_agents)
        aheaders = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                     'Connection': 'keep-alive',
                     #'GET': next_url,
                     'User-Agent': user_agent
                    }
        html = openurl(url, aheaders)
        html = html.decode('gb18030')

        # 頁數
        match_max_page = re.findall(r'共(\d+)页', html)
        if len(match_max_page) > 0:
            max_page = match_max_page[0]
        else:
            max_page=1
        print(max_page)
        page = int(max_page)

        while page != 0:
            #sleepRandom(2,2)
            if(page==1):
                next_url = url
            else:
                next_url = url + "/esfhouse/i3" + str(page) + "/"
            print(next_url)#esf.hnxa.fang.com/esfhouse/i32/

            user_agent = random.choice(user_agents)
            aheaders = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                         'Connection': 'keep-alive',
                         #'GET': next_url,
                         'User-Agent': user_agent
                        }
            html = openurl(next_url, aheaders)
            html = html.decode('gb18030')

            part = r'<p class="title"><a href="(.*?)"  {1,}target="_blank"'
            matchs = re.findall(part, html, re.S | re.M)
            if len(matchs) > 0:
                matchs = matchs[0]
            else:
                part = r'<a target="_blank" href="(\S+)" title='
                matchs = re.findall(part, html, re.S | re.M)
            print(matchs)#/cs/59.htm

            for match in matchs:
                #sleepRandom(1, 1)
                url_tmp = url + match
                user_agent = random.choice(user_agents)
                aheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Connection': 'keep-alive',
                            # 'GET': next_url,
                            'User-Agent': user_agent
                            }
                next_html = openurl(url_tmp, aheaders)
                next_html = next_html.decode('gb18030')

                code=""
                code_part = r'/view/(.*?).html'
                code_matchs = re.findall(code_part, match, re.S | re.M)
                if len(code_matchs) > 0:
                    code = code_matchs[0]

                title=""
                title_part = r'<title>(.*?)</title>'
                title_matchs = re.findall(title_part, next_html, re.S | re.M)
                if len(title_matchs) > 0:
                    title = title_matchs[0]
                print(title)

                price=""
                price_part = r'售 价：</span><span class="num30">(.*?)</span>万'
                price_matchs = re.findall(price_part, next_html, re.S | re.M)
                if len(price_matchs) > 0:
                    price = price_matchs[0]
                print(price)

                unitprice=""
                unitprice_part = r'</span>万（(.*?)/㎡）</dt>'
                unitprice_matchs = re.findall(unitprice_part, next_html, re.S | re.M)
                if len(unitprice_matchs) > 0:
                    unitprice = unitprice_matchs[0]
                print(unitprice)

                design=""
                design_part = r'户 型：</span>(.*?)</dd>'
                design_matchs = re.findall(design_part, next_html, re.S | re.M)
                if len(design_matchs) > 0:
                    design = design_matchs[0]
                    print(design_matchs)

                area=""
                area_part = r'建筑面积：</span>(.*?)㎡\r\n'
                area_matchs = re.findall(area_part, next_html, re.S | re.M)
                if len(area_matchs) > 0:
                    area = area_matchs[0]
                print(area)

                floor=""
                floor_part = r'楼 层：</span>(.*?)</dd>'
                floor_matchs = re.findall(floor_part, next_html, re.S | re.M)
                if len(floor_matchs) > 0:
                    floor = floor_matchs[0]
                print(floor)

                orientations=""
                orientations_part = r'朝 向：</span>(.*?)</dd>'
                orientations_matchs = re.findall(orientations_part, next_html, re.S | re.M)
                if len(orientations_matchs) > 0:
                    orientations = orientations_matchs[0]
                print(orientations_matchs)

                decoration=""
                decoration_part = r'装 修：</span>(.*?)</dd>'
                decoration_matchs = re.findall(decoration_part, next_html, re.S | re.M)
                if len(decoration_matchs) > 0:
                    decoration = decoration_matchs[0]
                print(decoration_matchs)

                age=""
                age_part = r'代：</span>(.*?)</dd>'
                age_matchs = re.findall(age_part, next_html, re.S | re.M)
                if len(age_matchs) > 0:
                    age = age_matchs[0]
                print(age)
#
#                 type=""
#                 type_part = r'<li {1,}class="pct50">物业：(.*?)</li>'
#                 type_matchs = re.findall(type_part, next_html, re.S | re.M)
#                 if len(type_matchs) > 0:
#                     type = type_matchs[0]
#
#                 village=""
#                 village_part_1 = r'小区：(.*?)</li>'
#                 village_matchs_1 = re.findall(village_part_1, next_html, re.S | re.M)
#
#                 village_part_2 = r'target="_blank">(.*?)</a>'
#                 village_matchs_2 = re.findall(village_part_2, village_matchs_1[0], re.S | re.M)
#                 if len(village_matchs_2) > 0:
#                     village = village_matchs_2[0]
#
#                 address = ""
#                 address_part = r'地址：(.*?)</ul>(.*?)<i class="corner"></i>'
#                 address_matchs = re.findall(address_part, next_html, re.S | re.M)
#
#                 if len(address_matchs) > 0:
#                     address_part_1 = r'>(.*?)</a>- {0,}(<a {1,}target="_blank" {1,}href="(.*?)"> (.*?) </a>&nbsp;&nbsp;)?(.*?)&nbsp;&nbsp;'
#                     address_matchs_1 = re.findall(address_part_1, str(address_matchs[0]), re.S | re.M)
#                     if len(address_matchs_1) > 0:
#                         address = city +" "+address_matchs_1[0][0] +" "+address_matchs_1[0][3]+" "+address_matchs_1[0][4]
#
#                 output[url_tmp] = city+'\tcode='+code+'\ttitle='+title+'\tprice='+price+'\tunitprice='+unitprice+'\tdownpay='+downpay+'\tmonpay='+monpay+'\tdesign='+design+'\tarea='+area+'\tage='+age+'\torientations='+orientations+'\tfloor='+floor+'\tdecoration='+decoration+'\ttype='+type+'\tvillage='+village+'\taddress='+address
#                 print(output)
#             page = page - 1
#         writeDictfile("output/output_%s.txt" % city, **output)
#         time_log("__"+ city +"__"+ "EEEEEEEEE_End")
#         print("@@@@@@@@@@@@@@@@@@@@@@@")