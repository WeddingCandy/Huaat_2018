
if __name__ == '__main__':
    list =['huize.com','http://www.pingan.com/','http://www.biqukan.com/1_1094/']
    req0 = requests.get(url=list[   0])
    req1 = requests.get(url=list[1])
    req2 = requests.get(url = list[2])
    html0 = req0.text
    html2 = req2.text

    # print(req.text)

    bf0 = BeautifulSoup(html0,"html.parser")
    bf2 = BeautifulSoup(html2 ,'html.parser')
    texts = bf0.find_all('div',id = 'content',class_ = 'showtxt')
    title_list = bf2.find_all('div' ,class_ = 'listmain')
    a_href = BeautifulSoup(str(title_list))
    a = a_href.find_all('a')
    for each in a:
        print(each.string, target + each.get('href'))
    print(texts[0].text.replace('\xa0'*8,'\n\n'))
    html1 = req1.text.decode('GBK')
    bf1 = BeautifulSoup(html1, "html.parser")
    contents = bf1.find_all('meta' ,name='keywords')
    print(contents)
    print(texts)


class downloader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'http://www.biqukan.com/1_1094/'
        self.names = []            #存放章节名
        self.urls = []            #存放章节链接
        self.nums = 0            #章节数

    def get_download_url(self):
        req = requests.get(url = self.target)
        html = req.text
        div_bf = BeautifulSoup(html,'html.parser')
        div = div_bf.find_all('div', class_ = 'listmain')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:])                                #剔除不必要的章节，并统计章节数
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2017-09-13
    """
    def get_contents(self, target):
        req = requests.get(url = target)
        html = req.text
        bf = BeautifulSoup(html,'html.parser')
        texts = bf.find_all('div', class_ = 'showtxt')
        texts = texts[0].text.replace('\xa0'*8,'\n\n') #\u3000是全角的空白符 ;\xa0 是不间断空白符 &nbsp
        return texts

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2017-09-13
    """
    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('《一年永恒》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '/Users/Apple/Desktop/一念永恒.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" %  float(i/dl.nums) + '\r')
        sys.stdout.flush()
