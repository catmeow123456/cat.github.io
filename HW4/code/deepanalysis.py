import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

words = [
    '弱智', '出院', '为什么',
    '水', '经验',
    '鸡', '意义', '问题', '人类',
    '地球', '太阳', '原神',
    '哲学',
]
symbols = [
    '感叹号',
    '问号',
    '句号',
    '逗号',
    '冒号',
    '顿号',
]

word_lib = []
ignore_words = ['人', '时', '主', '神', '水', '经验', '王', '手', '楼', '字', '事', '问', '话', '头', '牛']
for flag in ['vn', 'vd', 'n', 'nr', 'ns', 'ad', 'ag', 'an']:
    with open(f'./result/{flag}.txt', 'r') as f:
        linelist = f.readlines()
        for line in linelist:
            if ': ' not in line:
                continue
            word = line.split(': ')[0]
            times = int(line.split(': ')[1])
            if times < 500:
                continue
            if word in ignore_words:
                continue
            word_lib.append(word)

path = './outputs'
files = os.listdir(path)
file_size_list = []
for file in files:
    if not file.endswith('.txt') or not file.startswith('message'):
        continue
    size = os.path.getsize(os.path.join(path, file))
    file_size_list.append((file, size))
file_size_list.sort(key=lambda x: x[1], reverse=True)

num = 100
info = []
csv_title = ['id', 'size(byte)', '标题', '出现次数最多的词语']
for i in range(num):
    file, size = file_size_list[i]
    print(f'{file} size: {size} bytes')
    info.append([file.strip('message').strip('.txt'), size, "", ""])

csv_title.extend(words)
for i in range(num):
    print(f'进度：[{i+1}/{num}]')
    file, size = file_size_list[i]
    info[i].extend([0] * (len(words)))
    with open(os.path.join(path, file), 'r') as f:
        linelist = f.readlines()
        title = linelist[0].strip('\n ')
        if len(title) > 20:
            title = title[:17]+'...'
        info[i][2] = title
        info[i][3] = ""
        for line in linelist:
            for j, word in enumerate(words):
                info[i][j + 4] += line.count(word)
        tmp = [0] * len(word_lib)
        for line in linelist:
            for j, word in enumerate(word_lib):
                tmp[j] += line.count(word)
        # find the word that appears multiple times
        maxtimes = max(tmp)
        for j, times in enumerate(tmp):
            if times == maxtimes:
                info[i][3] = word_lib[j]
                break

csv_title.extend(symbols)
for i in range(num):
    file, size = file_size_list[i]
    info[i].extend([0] * len(symbols))
    with open(os.path.join(path, file), 'r') as f:
        linelist = f.readlines()
        for line in linelist:
            info[i][-6] += line.count('!') + line.count('！')
            info[i][-5] += line.count('?') + line.count('？')
            info[i][-4] += line.count('.') + line.count('。')
            info[i][-3] += line.count(',') + line.count('，')
            info[i][-2] += line.count(':') + line.count('：')
            info[i][-1] += line.count('、')

for i in range(num):
    print(info[i])
    assert len(info[i]) == len(csv_title)
df = pd.DataFrame(info, columns=csv_title)
df.to_csv('./analysis.csv', index=False, encoding='utf-8')

# 绘制 “弱智”、“出院”、“水”、“经验” 的直方图
plt.figure(figsize=(18, 12))
plt.rcParams['font.family'] = 'Heiti TC'
df.plot.bar(stacked=True, y=['水', '经验', '弱智', '出院', '问题'])
# 不显示横坐标
plt.xticks([])
plt.ylim(0, 2000)
# show
plt.title('最大的 100 条帖子中“弱智、出院、水、经验、问题”这些词语的出现次数')
# save figure
plt.savefig('./直方图.png')

plt.figure(figsize=(18, 12))
plt.title('关键词出现频率的相关系数')
df_corr = df[words].corr()
sns.heatmap(df_corr, vmax=0.4, vmin=0, center=0)
plt.savefig('./相关系数图.png')

# 计算标点符号的总出现次数
symbol_sum = df[symbols].sum()
# 绘制饼图
plt.figure(figsize=(12, 12))
plt.pie(symbol_sum, labels=symbols, autopct='%1.1f%%')
plt.title('标点符号的总出现次数占比图')
plt.savefig('./饼图.png')
