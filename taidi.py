import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import warnings
import datetime

# 读取附件1中的数据
data = pd.read_csv('C:\\Users\\MI\\Desktop\\泰迪杯A题\\数据\\附件1\\M101.csv')

# 时间戳
dates = data['日期']
times = data['时间']

# 创建一个新的列来保存转换后的结果
data['秒_小时'] = pd.to_datetime(times, unit='s').dt.strftime('%H:%M:%S')

# 获取当前年份
current_year = datetime.datetime.now().year

data['日期格式'] = pd.to_datetime(dates, format='%j').dt.strftime(f'{current_year}-%m-%d')

# 将日期和转换后的时间列合并成一个字符串列
data['时间戳'] = pd.to_datetime(data['日期格式'] + ' ' + data['秒_小时'])

# 将时间戳转换为 datetime 类型
data['时间戳'] = pd.to_datetime(data['时间戳'])

# 数据预处理
# 处理缺失值
data.fillna(0, inplace=True)

# 探索性数据分析（EDA）
# 统计各个装置故障字段的情况
fault_columns = ['物料推送装置故障1001', '物料检测装置故障2001', '填装装置检测故障4001',
                 '填装装置定位故障4002', '填装装置填装故障4003', '加盖装置定位故障5001',
                 '加盖装置加盖故障5002', '拧盖装置定位故障6001', '拧盖装置拧盖故障6002']

for column in fault_columns:
    print(f"故障{column}统计情况：")
    print(data[column].value_counts())

# 总操作数 总故障数
all_count = 0
fault_count = 0

# 每一个故障类型下对应的故障次数和正确次数
fault_column_count = []
right_column_count = []

# 将故障内容不为0的值全部置为1
for column in fault_columns:
    data[column] = data[column].apply(lambda x : 1 if x != 0 else x)

for column in fault_columns:
    data[column].value_counts()
    fault_count += data[column].value_counts()[1]
    all_count += data[column].value_counts()[0] + data[column].value_counts()[1]
    right_column_count.append(data[column].value_counts()[0])
    fault_column_count.append(data[column].value_counts()[1])

# 特征工程
# 计算故障率
data['故障总数'] = data[fault_columns].sum(axis=1)
data['故障率'] = data['故障总数'] / len(fault_columns)

# # 模型建立
# # 使用ARIMA模型进行时间序列预测
# # 这里以填装装置故障4003为例
# train_data = data['填装装置填装故障4003'].values
# model = ARIMA(train_data, order=(5, 1, 0))
# model_fit = model.fit()
#
# # 实时报警系统搭建
# # 判断是否需要报警
# # 假设设定阈值为0.5，超过阈值则触发报警
# threshold = 0.5
# if model_fit.forecast()[0] > threshold:
#     print("填装装置故障4003超过阈值，触发报警！")
# else:
#     print("填装装置故障4003未超过阈值，不触发报警。")

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 创建画布
plt.figure(figsize=(12, 6))

colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink', 'gray', 'brown']
width = 0.35

# 绘制故障状态的柱状图
plt.subplot(1, 2, 1)
plt.bar(range(len(fault_columns)), fault_column_count, width, color = colors)
plt.xticks(range(len(fault_columns)), fault_columns, rotation=45)
plt.title("故障状态统计情况")
plt.xlabel("故障状态")
plt.ylabel("频数")

# 绘制不故障状态的折线图
plt.subplot(1, 2, 2)
for column in fault_columns:
    normal_counts = data[data[column] == 0][column].value_counts().sort_index()
    plt.plot(normal_counts.index, normal_counts.values, marker='o', label=f"正常{column}")
plt.title("不故障状态统计情况")
plt.xlabel("故障状态")
plt.ylabel("频数")
plt.legend()

plt.tight_layout()
plt.show()

# 获取最小值和最大值
min_value = data['故障率'].min()
max_value = data['故障率'].max()

# 绘制故障率的时间序列图
plt.figure(figsize=(12, 6))
plt.plot(data['时间戳'], data['故障率'], marker='o', linestyle='-')
plt.title("故障率随时间变化趋势")
plt.xlabel("时间")
plt.ylabel("故障率")
plt.xticks(rotation=45)
plt.grid(True)
plt.ylim(0.1, 0.112)
plt.tight_layout()
plt.show()

#%%
