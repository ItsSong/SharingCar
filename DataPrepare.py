#!/usr/bin/env python
#-*- encoding = utf-8 -*-
# ----------------------------------------------------------
# Purpose:     聚类数据准备
# ----------------------------------------------------------
import pandas as pd
import pymysql

# 连接数据库
DBhost = '39.97.177.49'
DBuser = 'root'
DBpass = '123456'
DBname = 'testJZLJ'
try:
    conn = pymysql.connect(DBhost,DBuser,DBpass,DBname)
    print("数据库连接成功！")
except pymysql.Error as e:
    print("数据库连接失败！"+str(e))


# 从数据库中取数据
def read_data(cur,sql):
    try:
        cur.execute(sql)      # 执行sql语句
        data = cur.fetchall() # 获取全部数据
        data = pd.DataFrame(list(data)) # 转化数据格式：从数据库导入的数据格式为元组类型
        return data
    except:
        data = pd.DataFrame()
        print("错误e")
cur =  conn.cursor() #游标
mysql1 = "SELECT DISTINCT start_district_hash FROM AreaCompletePrice;"  # 每次只需要替换表格的名即可
distName = read_data(cur,mysql1)


# 取数据并存储至新的表（自定义格式）
c = []
for i in distName.iloc[:,0].tolist():
    hang = [0] * (144 * 16)
    mysql2 = "SELECT * FROM AreaCompletePrice WHERE start_district_hash='%s' ORDER BY TimePeriod;" % i
    temptable = read_data(cur,mysql2)
    t1 = temptable.iloc[:, 1].tolist() # 将第2列转化为list
    t3 = temptable.iloc[:,3].tolist()
    for index,j in enumerate(t1):
        if j>=(2304):
            pass
        else:
            hang[j]=t3[index]
    c.append(hang)
Value = pd.DataFrame(c).to_csv('ValueCompleteSeries.csv')
conn.close()

# 可视化58个区域的订单完成量
import matplotlib.pyplot as plt
df_com = pd.read_csv('ValueCompleteSeries.csv')
df_com1 = df_com.iloc[:,1:]
for i in range(58):
    area = df_com1.iloc[i,:].tolist()
    plt.plot(range(len(area)),area)
plt.show()

