# -*- coding = utf-8 -*-
# @Time : 2022/7/9 18:32
# @Author : yxz
# @File : test_urllib.py
# @Software : PyCharm

import urllib.request, urllib.error
import urllib.parse

# 获取一个get请求
response = urllib.request.urlopen("http://www.baidu.com")
print(response.read().decode("utf-8"))

# 获取一个post请求
# data = bytes(urllib.parse.urlencode({"hello":"world"}), encoding="utf-8")  # 将数据转化为二进制的数据包
# response = urllib.request.urlopen("http://httpbin.org/post", data=data)
# print(response.read().decode("utf-8"))


# 爬去超时处理，抛出异常
# try:
#     response = urllib.request.urlopen("http://httpbin.org/get", timeout=1)
#     print(response.read().decode("utf-8"))
# except urllib.error.URLError as e:
#     print("Time out!")


# response = urllib.request.urlopen("http://douban.com")
# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.status)
# print(response.getheaders())
# print(response.getheader("Server"))


# url = "https://www.douban.com"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49 "
# }
# data = bytes(urllib.parse.urlencode({'name': 'eric'}), encoding='utf-8')
# req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
# response = urllib.request.urlopen(req)
# print(response.read().decode("utf-8"))
