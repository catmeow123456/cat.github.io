import matplotlib.pyplot as plt

# 标点符号的名称
symbols = [
    '感叹号',
    '问号',
    '句号',
    '逗号',
    '冒号',
    '顿号',
]

res = [0] * 6
path = "./三国演义.txt"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()
    print(f'文本总长度：{len(text)}')
    # 统计标点符号
    res[0] += text.count('!') + text.count('！')
    res[1] += text.count('?') + text.count('？')
    res[2] += text.count('.') + text.count('。')
    res[3] += text.count(',') + text.count('，')
    res[4] += text.count(':') + text.count('：')
    res[5] += text.count('、')

plt.rcParams['font.family'] = 'Heiti TC'
plt.figure(figsize=(12, 12))
plt.pie(res, labels=symbols, autopct='%1.1f%%')
plt.title('标点符号的总出现次数占比图')
plt.show()
