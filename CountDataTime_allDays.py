#!/usr/bin/env python
#-*- encoding = utf-8 -*-
# -------------------------------------------------------------------------------
# Purpose:     统计每十分钟的订单请求量（时间）
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
def read_tabel(cur,sql):
    try:
        cur.execute(sql)       # 执行sql语句
        data = cur.fetchall()  # 获取全部数据
        data = pd.DataFrame(list(data))  # 将获取的数据转化为dataframe类型
        return data
    except:
        data = pd.DataFrame()
        print("错误e")

# 第三步：统计日订单请求量(10min为一个间隔）
cur = db.cursor()
sql = []      # 存储sql语句
mydata = []   # 存储执行sql语句的结果
beginTime=pd.Timestamp("2016-02-23 00:00:00")  # Timestamp()时间戳
allDays=23    # 总共有23天的数据
for i in range(144*allDays):  # 10min为一个间隔，每天144个时间段；
    # 以下注释这段代码为调试代码；程序运行中途出错时可以查看
    # if beginTime<=pd.Timestamp('2016-02-26 04:40:00'):
    #     endTime = beginTime + pd.Timedelta('0 days 00:10:00')
    #     beginTime = endTime
    #     continue
    endTime=beginTime+pd.Timedelta('0 days 00:10:00')    # Timedelta()实现datetime加减；这里是加10min
    s = "SELECT COUNT(passenger_id) FROM order_train WHERE Time>'%s' AND Time<='%s'" % (str(beginTime),str(endTime))
    sql.append(s)
    thisValue=read_tabel(cur,s)[0].iloc[0]  # df[0]表示取第0列向量；iloc[]表示将向量存储成列表(一维的时候）或者矩阵(二维时)；iloc[0]表示取列表的第一个数
    print(s)
    print(thisValue)
    mydata.append(thisValue)
    beginTime=endTime  # 更新开始时间，进行下一次循环

# 将运行的结果（每10min的订单请求量）存储至新的表里
df = pd.DataFrame(mydata,columns=['Requested order volume'])
df.to_csv('RequestedOrder_Time1.csv',encoding='utf-8')
db.close()

# #　第四步：可视化
# import matplotlib.pyplot as plt
# plt.plot(range(len(mydata)),mydata)
# plt.xlabel('Time Period')
# plt.ylabel('Requested order volume')
# plt.show()

