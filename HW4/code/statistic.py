import os
import jieba
import jieba.posseg as pseg

ignore_list = []

path = "./outputs/"
files = os.listdir(path)
files = [f for f in files if f.startswith('message') and f.endswith('.txt')]
data = {}
index = 0
for file in files:
    index += 1
    if (index % 10 == 0):
        print(f'进度： [{index}/{len(files)}]')
    with open(os.path.join(path, file), 'r') as f:
        linelist = f.readlines()
        for line in linelist:
            words = pseg.cut(line)
            for w in words:
                if w.word in ignore_list:
                    continue
                if not data.__contains__(w.flag):
                    data[w.flag] = {}
                if not data[w.flag].__contains__(w.word):
                    data[w.flag][w.word] = 0
                data[w.flag][w.word] += 1

# print the result and save to file

if not os.path.exists('./result'):
    os.mkdir('./result')

for flag in data.keys():
    data[flag] = dict(sorted(data[flag].items(), key=lambda x: x[1], reverse=True))
    with open(f'./result/{flag}.txt', 'w') as f:
        print('-'*50)
        print(f'flag: {flag}')
        for word in data[flag].keys():
            print(f'{word}: {data[flag][word]}')
            f.write(f'{word}: {data[flag][word]}\n')
