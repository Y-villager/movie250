# -*- coding = utf-8 -*-
# @Time : 2022/7/10 17:41
# @Author : yxz
# @File : testXlwt.py
# @Software : PyCharm


import xlwt

"""
workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet('sheet1')
worksheet.write(0,0,'testXlwt')    # 写入数据，第一个是行，第二个是列，第三个是值
workbook.save('./xls/testXlwt.xls')
"""

workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet('sheet1')
for i in range(0, 9):
    for j in range(0, i + 1):
        worksheet.write(i, j, "%d * %d = %d" % (j + 1, i + 1, (i + 1) * (j + 1)))

workbook.save('./xls/testXlwt.xls')


