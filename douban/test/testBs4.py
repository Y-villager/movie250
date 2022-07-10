# -*- coding = utf-8 -*-
# @Time : 2022/7/9 19:45
# @Author : yxz
# @File : testBs4.py
# @Software : PyCharm

"""
Beautifulsoup4 将复杂的html文档转化成一个复杂的树状结构，每个节点都是python对象，都有对象可以归纳为以下四类：
- Tag
- NavigableString
- Beautifulsoup
- Comment
"""
import re

from bs4 import BeautifulSoup

file = open("./baidu.html", "rb")
html = file.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")
# 1.Tag 标签及其内容；拿到它所找到的第一个内容
# print(bs.a)
# print(type(bs.head))

# 2.NavigableString 标签里的内容、属性（字符串）
# print(bs.a.attrs)

# 3.
# print(type(bs))     # 表示整个文档
# print(bs)

# 4.Comment
# print(bs.a.string)


# 文档的遍历
print(bs.head.contents[1])  # 获取文件数组

# 文档的搜索
# 1.find_all()

# 字符串过滤：会查找与字符串完全匹配的内容
# t_list = bs.find_all("a")
# print(t_list)

import re


# 正则表达式搜索：使用search()方法来匹配内容
# t_list = bs.find_all(re.compile("a"))
# print(t_list)

# 方法搜索：传入一个函数，根据函数搜索
# def name_is_exists(tag):
#     return tag.has_attr("name")
#
#
# t_list = bs.find_all(name_is_exists)


# 2.kwargs 参数
# t_list = bs.find_all(id="head")
# t_list = bs.find_all(class_=True)
# for item in t_list:
#     print(item)


# 3.text参数
# t_list = bs.find_all(text="hao123")
# t_list = bs.find_all(text=[hao123", "贴吧", "地图"])
# for item in t_list:
#     print(item)


# 4.limit 参数
# t_list = bs.find_all("a", limit=3)
# for item in t_list:
#     print(item)


# css选择器
# t_list = bs.select('title')     # 通过标签来查找
# t_list = bs.select(".mnav")     # 通过类名来查找
# t_list = bs.select("#u1")       # 通过id来查找
# t_list = bs.select("a[class='bri']")    # 通过属性查找
t_list = bs.select("haed > title")      # 通过子标签查找
for item in t_list:
    print(item)

