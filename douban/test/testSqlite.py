# -*- coding = utf-8 -*-
# @Time : 2022/7/10 18:54
# @Author : yxz
# @File : testSqlite.py
# @Software : PyCharm


import sqlite3

# 1.创建数据库
conn = sqlite3.connect("test.db")
print("Open Database Successfully")


# 2.创建表
"""
c = conn.cursor()   # 获取游标
sql = '''
    create table company
    (id int primary key not null,
    name text not null,
    age int not null,
    address text not null,
    salary real);
'''

c.execute(sql)  # 执行sql语句
conn.commit()   # 提交数据库操作
conn.close()    # 关闭数据库连接

print("Create table successfully")
"""


# 3.查询数据
"""

sql1 = '''
    insert into company (id,name,age,address,salary)
    values (1,'张三',32,"成都",8000)
'''

sql2 = '''
    insert into company (id,name,age,address,salary)
    values (2,'李四',42,"台州",5000)
'''
c.execute(sql1)
c.execute(sql2)
conn.commit()
conn.close()

print("Create table successfully")
"""


# 4.查询数据
c = conn.cursor()   # 创建游标
sql = "Select id,name,address,salary from company"
cursor = c.execute(sql)
for row in cursor:
    print("id = ", row[0])
    print("name = ", row[1])
    print("address = ", row[2])
    print("salary = ", row[3], "\n")

conn.close()
print("查询完毕")
