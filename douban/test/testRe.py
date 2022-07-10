# -*- coding = utf-8 -*-
# @Time : 2022/7/10 15:24
# @Author : yxz
# @File : testRe.py
# @Software : PyCharm


# 正则表达式：字符串模式（判断字符串是否符合判断标准）
import re


# 创建模式对象
pat = re.compile("AA")
# m = pat.search("CBA")  # search字符串被校验的内容
# print(m)
# m = pat.search("CBAa")
# print(m)
# m = pat.search("CBAA")
# print(m)
# m = pat.search("CBAAabcAA")  # search方法，进行比对查找
# print(m)


# 没有模式对象
# m = re.search("asd", "Aasd")    # 前面的字符串是规则（模板），后面的字符串是校验对象
# print(m)


# print(re.findall("a","ASDaDEFGAa"))     # 找出所有“a”成一个列表
# print(re.findall("[A-Z]", "ASDaDEFGAa"))     # 根据正则表达式搜索
# print(re.findall("[A-Z]+", "ASDaDEFGAa"))     #


# sub
# print(re.sub("a", "A", "abcdcasd"))     # 将a替换为A


# 建议在正则表达式中，将比较的字符串前面加上r，不用担心转义字符
# a = "\aabd-\'"  # abd-'
# a = r"\aabd-\'"
# print(a)

