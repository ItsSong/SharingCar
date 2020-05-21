#!/usr/bin/env python
#-*- encoding = utf-8 -*-
# -------------------------------------------------------------------------------
# Purpose:     将一个文件目录下的所有txt文件存储至一个csv中
# -------------------------------------------------------------------------------

# 第一步：将所有txt文件名存储在一个列表里
import os
path = 'C:/Users/宋宝宝/Desktop/网约车/数据/滴滴/test_set/traffic_data'
dirList = os.listdir(path) # 将path文件目录下的所有文件存为一个列表
print(dirList[0]) # 验证：查看一下该目录下第一个文件
newFile=open("traffic_test.csv","a")

# 第二步：依次读取列表中文件的内容
for i in range(len(dirList)):
    f = open(path + '\\' + dirList[i])  # 每一个txt的路径+文件名；双斜杠表示为\的转义
    for line in f:
        line = line.split('\t')
        newLine = ''
        for i in range(len(line)-1):
            newLine += line[i]
            newLine += ','
        newLine +=line[-1]
        newFile.write(newLine)

newFile.close()




# filename = 'C:/Users/宋宝宝/Desktop/网约车/数据/滴滴/training_set/order_data/order_data_2016-02-23.txt'
# xlsname = 'C:/Users/宋宝宝/Desktop/网约车/数据/滴滴/training_set/order_data/order_data_2016-02-23'




