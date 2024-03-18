from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import jieba.posseg as pseg
from pyecharts.charts import Page


src_filename = "./data/hw1-3.txt"
word_dict = {}
word_dict_2 = {}

with open(file=src_filename, mode="r") as file:
    strs = file.readlines()
    print(f'the total number of lines of file \"{src_filename}\" is {len(strs)}.')
    index = 0
    for str in strs:
        index = index + 1
        print(f'[{index}/{len(strs)}]')
        words = pseg.cut(str)
        for w in words:
            if w.flag in ['a','c','n','nr','ns','v']:
                if not word_dict.__contains__(w.word):
                    word_dict[w.word] = 0
                word_dict[w.word] = word_dict[w.word] + 1
            if w.flag in ['n','nr','ns']:
                if not word_dict_2.__contains__(w.word):
                    word_dict_2[w.word] = 0
                word_dict_2[w.word] = word_dict_2[w.word] + 1

print('word_dict is generated successfully')

words = list(word_dict.items())
words2 = list(word_dict_2.items())

cloud = WordCloud()
cloud = cloud.add('', words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
cloud = cloud.set_global_opts(title_opts=opts.TitleOpts(title="魔道祖师小说词频统计（形容词+连词+名词+人名+地名+动词"))

cloud2 = WordCloud()
cloud2 = cloud2.add('', words2, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
cloud2 = cloud2.set_global_opts(title_opts=opts.TitleOpts(title="魔道祖师小说词频统计（名词+人名+地名）"))

page = Page(layout=Page.SimplePageLayout)
page.add(
    cloud,
    cloud2
)
page.render("hw1-3.html")