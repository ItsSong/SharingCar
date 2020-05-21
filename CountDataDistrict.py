#!/usr/bin/env python
#-*- encoding = utf-8 -*-
# -------------------------------------------------------------------------------
# Purpose:     统计每个地区的订单请求量（空间）
# -------------------------------------------------------------------------------

# 第一步：连接数据库
import pymysql
DBhost = '39.97.177.49'
DBuser = 'root'
DBpass = '123456'
DBname = 'testJZLJ'
try:
    db = pymysql.connect(DBhost,DBuser,DBpass,DBname)
    print("数据库连接成功！")
except pymysql.Error as e:
    print("数据库连接失败！"+str(e))


# 第二步：将导入的数据转换为pandas库可以操作的类型，即dataframe
import pandas as pd
import traceback
def read_tabel(cur,sql):
    try:
        cur.execute(sql)       # 执行sql语句
        data = cur.fetchall()  # 获取全部数据

        data = pd.DataFrame(list(data))  # 将获取的数据转化为dataframe类型
        return data
    except:
        traceback.print_exc()
        data = pd.DataFrame()
        print("错误e")

# 第三步：统计每个地区的订单请求量（每10min)


sql = []   # 存储sql语句
mydata = pd.DataFrame()  # 存储执行sql语句的结果
for k in [23]:  # 先统计23号和24号两天的
    for j in range(0,24):  # 从0点开始，直到24点结束
        cur = db.cursor()
        for i in range(6): # 每10分钟统计一次，一小时6个十分钟
            if i == 5:     # 当i=5时，不是0:60：00；而是01:00:00
                s="SELECT COUNT(passenger_id),start_district_hash FROM order_train WHERE Time>'2016-02-%s %s:%s:00' AND Time<='2016-02-%s %s:%s:00' GROUP BY start_district_hash" % (k,j,i * 10,k,j+1,0)
            else:
                s = "SELECT COUNT(passenger_id),start_district_hash FROM order_train WHERE Time>'2016-02-%s %s:%s:00' AND Time<='2016-02-%s %s:%s:00' GROUP BY start_district_hash" % (k,j, i * 10,k, j, (i + 1) * 10)
            sql.append(s)
            thisValue=read_tabel(cur,s)
            print(s)
            print(thisValue)
            mydata = pd.concat([mydata,thisValue])  # 合并DataFrame
        cur.close()

mydata.to_csv('RequestedOrder_District.csv',encoding='utf-8')
db.close()

# #　第四步：可视化
# import matplotlib.pyplot as plt
# plt.plot(range(len(mydata.iloc[:,0])),mydata.iloc[:,0])
# plt.xlabel('District')
# plt.ylabel('Requested order volume')
# plt.show()


