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
    if flag not in ['vn', 'vd', 'n', 'nr', 'ns', 'a', 'ad', 'ag', 'an']:
        continue
    with open(os.path.join(path, file), 'r') as f:
        linelist = f.readlines()
        for line in linelist:
            if ': ' not in line:
                continue
            word = line.split(': ')[0]
            count = int(line.split(': ')[1])
            words.append((f"{file.strip('.txt')}:{word}", count))

cloud = WordCloud()
cloud = cloud.add('', words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
cloud = cloud.set_global_opts(title_opts=opts.TitleOpts(title="贴吧\"弱智吧\"词频统计图"))

page = Page(layout=Page.SimplePageLayout)
page.add(
    cloud
)
page.render("词频图.html")
