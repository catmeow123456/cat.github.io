# 这个代码对 ./code/outputs 文件夹下的帖子内容做进一步的分析。
# 确定了几个关键词，并研究了这些关键词在帖子中的出现次数，它们的相关系数，标点符号在帖子中分布的占比等等。

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 关键词
words = [
    '弱智', '出院', '为什么',
    '水', '经验',
    '鸡', '意义', '问题', '人类',
    '地球', '太阳', '原神',
    '哲学',
]
# 标点符号的名称
symbols = [
    '感叹号',
    '问号',
    '句号',
    '逗号',
    '冒号',
    '顿号',
]

word_lib = []
# 忽略的词语的列表
ignore_words = ['人', '时', '主', '神', '水', '经验', '王', '手', '楼', '字', '事', '问', '话', '头', '牛']
# 获取高频词语的列表，存入 word_lib，用于分析帖子的最高频词语。
for flag in ['vn', 'vd', 'n', 'nr', 'ns', 'ad', 'ag', 'an']:  # 枚举我们关注的词性（名次、动词、形容词）
    with open(f'./result/{flag}.txt', 'r') as f:  # 读取相应的词性文件
        linelist = f.readlines()
        for line in linelist:
            if ': ' not in line:
                continue
            word = line.split(': ')[0]
            times = int(line.split(': ')[1])
            # 如果出现次数太少，就直接忽略
            if times < 500:
                continue
            # 如果出现在忽略列表中，也直接忽略
            if word in ignore_words:
                continue
            # 加入 word_lib
            word_lib.append(word)

# 读取 outputs 文件夹下的所有 message 开头的 txt 文件
# 将文件名、文件大小存入 file_size_list
path = './outputs'
files = os.listdir(path)
file_size_list = []
for file in files:
    if not file.endswith('.txt') or not file.startswith('message'):
        continue
    size = os.path.getsize(os.path.join(path, file))
    file_size_list.append((file, size))
# 按照文件大小从大到小排序
file_size_list.sort(key=lambda x: x[1], reverse=True)

# 关注数据量最大的 100 个帖子，后续将这些帖子的统计结果存入 info
# info 是一个二维的列表，每一行代表一个帖子的统计结果，csv_title 是 info 的列名
num = 100
info = []
csv_title = ['id', 'size(byte)', '标题', '出现次数最多的词语']
for i in range(num):
    file, size = file_size_list[i]
    print(f'{file} size: {size} bytes')
    info.append([file.strip('message').strip('.txt'), size, "", ""])

# 统计关键词的出现次数
csv_title.extend(words)
for i in range(num):
    print(f'进度：[{i+1}/{num}]')
    file, size = file_size_list[i]
    # 添加 len(words) 列
    info[i].extend([0] * (len(words)))
    with open(os.path.join(path, file), 'r') as f:
        linelist = f.readlines()
        # 获取帖子标题
        title = linelist[0].strip('\n ')
        if len(title) > 20:
            title = title[:17]+'...'
        # 第二列是标题
        info[i][2] = title
        # 第三列是当前帖子中出现次数最多的词语
        info[i][3] = ""
        # 第 4 到 4+len(words)-1 列代表每一个关键词的出现次数
        for line in linelist:
            for j, word in enumerate(words):
                info[i][j + 4] += line.count(word)
        # 接下来，求出现次数最多的词语（主题词）
        # 预处理 tmp 数组，遍历 word_lib 中的每一个词语，统计其出现次数
        tmp = [0] * len(word_lib)
        for line in linelist:
            for j, word in enumerate(word_lib):
                tmp[j] += line.count(word)
        # 取出其中出现次数最多的词语
        maxtimes = max(tmp)
        for j, times in enumerate(tmp):
            if times == maxtimes:
                info[i][3] = word_lib[j]
                break

# 统计标点符号的出现次数
csv_title.extend(symbols)
for i in range(num):
    file, size = file_size_list[i]
    # 添加六列
    info[i].extend([0] * len(symbols))
    with open(os.path.join(path, file), 'r') as f:
        linelist = f.readlines()
        for line in linelist:
            # 标点符号的中文和英文是不同的，这里一起统计
            info[i][-6] += line.count('!') + line.count('！')
            info[i][-5] += line.count('?') + line.count('？')
            info[i][-4] += line.count('.') + line.count('。')
            info[i][-3] += line.count(',') + line.count('，')
            info[i][-2] += line.count(':') + line.count('：')
            info[i][-1] += line.count('、')

# 输出 info 到 terminal
for i in range(num):
    print(info[i])
    assert len(info[i]) == len(csv_title)
# 创建 pandas 的 DataFrame 数据结构，并保存到 analysis.csv 文件中
df = pd.DataFrame(info, columns=csv_title)
df.to_csv('./analysis.csv', index=False, encoding='utf-8')

# 绘制 “弱智”、“出院”、“水”、“经验” 的直方图
plt.figure(figsize=(18, 12))
plt.rcParams['font.family'] = 'Heiti TC'
df.plot.bar(stacked=True, y=['水', '经验', '弱智', '出院', '问题'])
plt.xticks([])  # 不显示横坐标
plt.ylim(0, 2000)  # 设置纵坐标范围
plt.title('最大的 100 条帖子中“弱智、出院、水、经验、问题”这些词语的出现次数')  # 设置标题
plt.savefig('./直方图.png')

# 绘制关键词出现频率的相关系数
plt.figure(figsize=(18, 12))
plt.title('关键词出现频率的相关系数')
df_corr = df[words].corr()
sns.heatmap(df_corr, vmax=0.4, vmin=0, center=0)
plt.savefig('./相关系数图.png')

# 计算标点符号的总出现次数
symbol_sum = df[symbols].sum()
# 绘制标点符号分布占比的饼图
plt.figure(figsize=(12, 12))
plt.pie(symbol_sum, labels=symbols, autopct='%1.1f%%')
plt.title('标点符号的总出现次数占比图')
plt.savefig('./饼图.png')
