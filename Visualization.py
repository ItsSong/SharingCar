#!/usr/bin/env python
#-*- encoding = utf-8 -*-
# ----------------------------------------------------------
# Purpose:     对比：订单完成量 + 订单请求量（时间维度）
# ----------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# 所有订单完成量
df_c = pd.read_csv('CompletedOrder_time_train.csv',encoding='utf-8')
ax = df_c.plot(x='TimePeriod',y='COUNT(driver_id)',legend='Completed Order Volume')
# 所有订单请求量
df_r = pd.read_csv('RequestOrder_time_train.csv',encoding='utf-8')
df_r.plot(x='TimePeriod',y='COUNT(order_id)',legend='Request Order Volume',ax=ax) # ax=ax表示在第一张图的窗口继续叠加（画在一个窗口）
plt.show()
