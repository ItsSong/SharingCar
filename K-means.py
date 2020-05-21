#!/usr/bin/env python
#-*- encoding = utf-8 -*-
# ----------------------------------------------------------
# Purpose:     划分聚类：K-means
# ----------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 读数据
df = pd.read_csv('ValueCompleteSeries.csv', header=0, encoding='utf-8')
df1 = df.iloc[:,1:]

# 利用SSE选择聚类数：k
SSE = []
for k in range(1, 10):
    estimator = KMeans(n_clusters=k)
    estimator.fit(np.array(df1))
    SSE.append(estimator.inertia_)
X = range(1, 10)
plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(X, SSE, 'o-')
plt.show()

# 聚类（根据上图显示k=4聚类效果最好）
model = KMeans(n_clusters=4, n_jobs=4, max_iter=100)  # 聚3类、并发数4、最大循环次数100
model.fit(df1)
# 简单打印结果
r1 = pd.Series(model.labels_).value_counts() # 统计各个类别的数据
r2 = pd.DataFrame(model.cluster_centers_)    # 找出聚类中心
r = pd.concat([r2,r1],axis=1)                # 横向连接（0是纵向），得到聚类中心对应的类别下的数
r.columns = list(df1.columns) + [u'类别数目'] # 重命名表头
print(r)
# 详细输出原始数据及其类别
r = pd.concat([df1, pd.Series(model.labels_, index=df1.index)], axis=1)
r.columns = list(df1.columns) + [u'聚类类别']
r.to_csv('df1Tpye.csv')


# # 绘制聚类后的概率密度图
# def density_plot(data,title):
#     plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
#     plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号
#     plt.figure()
#     for i in range(len(data.iloc[0])): # 逐列作图
#         (data.iloc[:,i]).plot(kind='kde', label = data.columns[i], linewidth = 2)
#     plt.ylabel(u'density')
#     plt.xlabel(u'Timeperiod')
#     plt.title(u'聚类类别%s各属性的密度曲线'% title)
#     plt.legend()
#     return plt
#
# def density_plot(data):
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#     plt.rcParams['axes.unicode_minus'] = False
#     p = data.plot(kind='kde', linewidth = 2, subplots = True, sharex = False)
#     [p[i].set_ylabel(u'density') for i in range(3)]
#     plt.legend()
#     return plt
#
# pic_output = 'pd_'  # 图存储的前缀名
# for i in range(3):
#     density_plot(df1[r[u'聚类类别']==i]).savefig(u'%s%s.png' % (pic_output, i))

