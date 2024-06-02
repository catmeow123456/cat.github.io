# 这个代码对 ./code/outputs 文件夹下的帖子内容做初步分析
# 用于统计所有帖子内容分词后的词频，将结果保存到 result 文件夹下
# 每个文件对应一个词性，文件中每行为一个词和它的出现次数

import os
import jieba.posseg as pseg

# 取出 outputs 文件夹下所有 message 开头的 txt 文件名
path = "./outputs/"
files = os.listdir(path)
files = [f for f in files if f.startswith('message') and f.endswith('.txt')]
# 初始化空字典
data = {}
index = 0
for file in files:
    index += 1
    # 显示进度
    if (index % 10 == 0):
        print(f'进度： [{index}/{len(files)}]')
    # 读取帖子文件内容
    with open(os.path.join(path, file), 'r') as f:
        linelist = f.readlines()
        # 用 pseg.cut 对每一行进行分词
        for line in linelist:
            words = pseg.cut(line)
            # 将分词结果存入字典 data
            for w in words:
                if not data.__contains__(w.flag):
                    data[w.flag] = {}
                if not data[w.flag].__contains__(w.word):
                    data[w.flag][w.word] = 0
                # 更新出现次数
                data[w.flag][w.word] += 1

# 将结果写入文件
if not os.path.exists('./result'):
    os.mkdir('./result')

# 枚举词性
for flag in data.keys():
    # 按出现次数从大到小排序
    data[flag] = dict(sorted(data[flag].items(), key=lambda x: x[1], reverse=True))
    # 写入文件
    with open(f'./result/{flag}.txt', 'w') as f:
        print('-'*50)
        print(f'flag: {flag}')
        for word in data[flag].keys():
            print(f'{word}: {data[flag][word]}')
            f.write(f'{word}: {data[flag][word]}\n')
