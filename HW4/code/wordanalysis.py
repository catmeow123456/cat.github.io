# 这个代码对 wordstatistic.py 运行结果进行可视化，生成词频统计图

import os
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts.charts import Page

path = './result/'
files = os.listdir(path)
words = []
for file in files:
    flag = file.strip('.txt')
    # 只关注动词、名次、形容词和相近的词性
    if flag not in ['vn', 'vd', 'n', 'nr', 'ns', 'a', 'ad', 'ag', 'an']:
        continue
    # 读取相应的词性文件中所有的词语和出现次数
    with open(os.path.join(path, file), 'r') as f:
        linelist = f.readlines()
        for line in linelist:
            # 每一行的格式是 word: count，将其分割开
            if ': ' not in line:
                continue
            word = line.split(': ')[0]
            count = int(line.split(': ')[1])
            # 按照 (flag: word, count) 格式保存进 words 列表
            words.append((f"{file.strip('.txt')}:{word}", count))

# 生成词云图
cloud = WordCloud()
cloud = cloud.add('', words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
cloud = cloud.set_global_opts(title_opts=opts.TitleOpts(title="贴吧\"弱智吧\"词频统计图"))

# 渲染页面保存结果
page = Page(layout=Page.SimplePageLayout)
page.add(
    cloud
)
page.render("词频图.html")
