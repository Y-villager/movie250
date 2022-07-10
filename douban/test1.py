# -*- coding = utf-8 -*-
# @Time : 2022/7/9 18:13
# @Author : yxz
# @File : test1.py
# @Software : PyCharm

import random
import re  # 正则
import bs4  # 网页解析
from bs4 import BeautifulSoup
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLite数据库操作
import xlrd

# 免费代理IP不能保证永久有效，如果不能用可以更新
proxy_list = [
    {'http': '118.163.120.181:58837'},
    {'http': '58.20.235.180:9091'},
    {'http': '202.55.5.209:8090'},
    {'http': '47.56.69.11:8000'},
]

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]

# 影片详情链接规则
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则
# 影片图片链接规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S让换行符包括在字符中
# 影片标题
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 影评人数
findRating_num = re.compile(r'<span>(\d*)人评价</span>')
# 概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 影片相关内容
findBd = re.compile('<p class="">(.*?)</p>', re.S)


def getData2Exc(savepath):
    data = xlrd.open_workbook(savepath)
    sheet = data.sheet_by_name('豆瓣电影top250')
    datalist = []
    for r in range(1, sheet.nrows):
        d = []
        for c in range(sheet.ncols):
            d.append(sheet.cell_value(r, c))
        datalist.append(list(d))
    # print(datalist[:10])
    return datalist


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬去网页
    # datalist = getData(baseurl)
    savepath = ".\\豆瓣电影250.xls"
    dbpath = "movietest.db"  # 数据库路径

    # 获取数据
    datalist = getData2Exc(savepath)

    # 3.保存数据
    saveData2DB(datalist, dbpath)


# 保存数据到数据库
def saveData2DB(datalist, dbpath):
    # init_db(dbpath)
    print(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250(
            info_link, pic_link, cname, ename, score, rating, introduction, info)
            values(%s)''' % ",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
        Create table movie250(
            id integer primary key autoincrement,
            info_link text,
            pic_link text,
            cname varchar,
            ename varchar,
            score numeric(2,1),
            rating numeric,
            introduction text,
            info text
        )
    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 爬取网页
def getData(baseurl):
    datalist = []
    # 2.逐一解析网页源码
    for i in range(0, 10):  # 调用获取页面函数，10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取的网页源码

        soup = BeautifulSoup(html, "html.parser")  # 解析网页内容
        for item in soup.find_all('div', class_="item"):
            # print(item)
            data = []
            item = str(item)

            # 1.详情链接
            link = re.findall(findLink, item)[0]
            data.append(link)

            # 2.图片链接
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)

            # 3.中文标题
            # 4.外文标题
            titles = re.findall(findTitle, item)  # 片名可能只有一个中文名，没有外国名
            if len(titles) == 2:
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉不相关的符号
                otitle = otitle.replace(" ", "")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')  # 外国名留空

            # 5.影评
            rating = re.findall(findRating, item)[0]
            data.append(rating)

            # 6.影评人数
            rating_num = re.findall(findRating_num, item)[0]
            data.append(rating_num)

            # 7.概述
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(inq)

            # 8.相关信息
            bd = re.findall(findBd, item)[0]
            # bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', '', bd)
            data.append(bd.strip())

            datalist.append(data)

    return datalist


# 得到指定url的网页内容
def askURL(url):
    head = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    html = ""
    # 随机选择一个IP
    proxy_ip = random.choice(proxy_list)
    print(proxy_ip)

    proxy_handler = urllib.request.ProxyHandler(proxy_ip)
    opener = urllib.request.build_opener(proxy_handler)
    print(url)
    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        # response = opener.open(request)
        html = response.read().decode("utf-8")
        return html
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e)
        if hasattr(e, "reason"):
            print(e)


# 保存数据
def saveData(savepath, datalist):
    print("saving---------")
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "影片中文名", "影片英文名", "影评", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        worksheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            worksheet.write(i + 1, j, data[j])
    workbook.save(savepath)


if __name__ == '__main__':
    # init_db("movietest.db")
    main()
    print("爬取完毕------")
