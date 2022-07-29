# -*- coding = utf-8 -*-
# @Time : 2022/7/9 18:13
# @Author : yxz
# @File : main.py
# @Software : PyCharm

import re  # 正则
import time
from pathlib import Path
import openpyxl as openpyxl
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
from lxml import etree
import xlrd
from xlutils.copy import copy
import os

# 创建文件夹
d_path = r"E:\Downloads\迅雷下载"


# 获取excel表里数据
def getDataExc(savepath, colname):
    data = xlrd.open_workbook(savepath)
    sheet = data.sheet_by_name(colname)
    datalist = []
    for r in range(1, sheet.nrows):
        d = []
        for c in range(sheet.ncols):
            d.append(sheet.cell_value(r, c))
        datalist.append(list(d))
    # print(datalist[:10])
    return datalist


# 保存数据到excel表
def saveDataExc(savepath, datalist, colname, sheetname):
    print("saving---------")
    # 1.创阿工作蒲
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 2.创建sheet表单
    worksheet = workbook.add_sheet(sheetname, cell_overwrite_ok=True)  # 创建工作表
    # 3.写表头
    worksheet.write(0, 0, colname)
    # 图片张数
    nums = len(datalist)
    # 4.添加内容
    for i in range(0, nums):
        # print("第%d张图" % (i + 1))
        worksheet.write(i + 1, 0, datalist[i])
    workbook.save(savepath)
    print("写入excel成功")


def appendToExcel(filename, words, head):
    # 打开excel
    word_book = xlrd.open_workbook(filename)
    # 获取所有的sheet表单。
    sheets = word_book.sheet_names()
    # 获取第一个表单
    work_sheet = word_book.sheet_by_name(sheets[0])
    # 获取已经写入的列数
    old_col = work_sheet.ncols
    # 将xlrd对象变成xlwt
    new_work_book = copy(word_book)
    # 添加内容
    new_sheet = new_work_book.get_sheet(0)
    c = old_col
    # 表头
    new_sheet.write(0, c, head)
    for i in range(0, len(words)):
        # print("第%d张图" % (i + 1))
        new_sheet.write(i+1 , c, words[i])
    new_work_book.save(filename)
    print('追加成功！')


def getLocalData():
    print("getLocal----")
    s = "SSSSSS"
    list = []
    for i in range(3):
        list.append(s)

    print(list)
    return list


def main(savepath, baseurl, colname, sheetname):
    # 获取数据
    datalist = getData(baseurl)
    # datalist = getLocalData()

    # 文件是否存在
    file_path = Path(savepath)

    # 下载的文件夹是否存在
    # down_path = Path(d_path + r"/"+colname)
    # if down_path.exists():
    #     print("文件夹已经创建了")
    #     pass
    # else:
    #     print("文件夹不存在，创建中--")
    #     os.mkdir(d_path+r"/"+colname)

    if file_path.exists():
        appendToExcel(savepath, datalist, colname)
    else:
        saveDataExc(savepath, datalist, colname, sheetname)


# 爬取网页
def getData(baseurl):
    print("获取 "+baseurl+" 网页信息---")
    datalist = []
    html = etree.HTML(askURL(baseurl))

    # nums = html.xpath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/h5[5]/div')
    nums = html.xpath('//div[@class="comics-metadata-margin-top"]/h5/div/text()')[0]
    nums = int(nums)

    url = baseurl + "/1"
    html = etree.HTML(askURL(url))
    imgUrl = str(html.xpath('//*[@id="current-page-image"]/@src')[0])
    pattern = re.compile(r'(\d)*.jpg')
    for i in range(nums):
        name = str(i+1) + ".jpg"
        imgUrl = re.sub(pattern, name, imgUrl)
        datalist.append(imgUrl)
        # imgUrl = imgUrl.
    return datalist


# 得到指定url的网页内容
def askURL(url):
    print("获取网页内容中-------")
    head = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/103.0.0.0 Safari/537.36"}
    html = ""
    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        # response = opener.open(request)
        html = response.read().decode("utf-8")
        response.close()
        time.sleep(1)
        return html
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e)
        if hasattr(e, "reason"):
            print(e)


if __name__ == '__main__':
    # 爬取漫画的页面
    # 1.保存excel文件位置
    savepath = ".\\ComicPath.xls"
    sheetname = "Comic"
    colname = ["求爱异乡人", "想隐瞒之事"]
    baseurl =["https://hanime1.me/comic/2290", "https://hanime1.me/comic/410"]
    # comic_url = {"求爱异乡人": "https://hanime1.me/comic/2290", "想隐瞒之事": "https://hanime1.me/comic/410"}
    i = 0
    for c in colname:
        main(savepath, baseurl[i], c, sheetname)
        i += 1
