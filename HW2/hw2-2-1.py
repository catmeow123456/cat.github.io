import jieba
import jieba.posseg as pseg
import os
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts.charts import Page

if not os.path.exists('./output'):
    os.makedirs('./output')
# 输入文件
src_filename = "./data/hw2-2.txt"

# 输出文件
node_file_name = './output/魔道祖师-人物节点-分类.csv'
link_file_name = './output/魔道祖师-人物连接.csv'

# 加载用户字典
jieba.load_userdict('./data/userdict.txt')
# 设置忽略词的列表
category = {
    '魏婴': '云梦江氏',
    '江澄': '云梦江氏',
    '蓝湛': '姑苏蓝氏',
    '蓝曦臣': '姑苏蓝氏',
    '金光瑶': '兰陵金氏',
    '金凌': '兰陵金氏',
    '金光善': '兰陵金氏',
    '孟瑶': '兰陵金氏',
    '温宁': '岐山温氏',
    '温晁': '岐山温氏',
    '聂明诀': '清河聂氏',
    '蓝思追': '姑苏蓝氏',
    '聂怀桑': '清河聂氏',
    '蓝景仪': '姑苏蓝氏',
}
ignore_list = ['蓝氏', '金氏', '温氏', '江氏', '金麟', '金麟台']

word_dict = {}
linelist = []

# --- 第1步：生成基础数据（一个列表，一个字典）
line_name_list = []  # 每个段落出现的人物列表

with open(file=src_filename, mode="r") as file:
    linelist = file.readlines()
    print(f'the total number of lines of file \"{src_filename}\" is {len(linelist)}.')
    index = 0
    for line in linelist:
        index = index + 1
        line_name_list.append([])
        print(f'[{index}/{len(linelist)}]')
        words = pseg.cut(line)
        for w in words:
            if len(w.word) == 1:
                continue
            if w.word in ignore_list:
                continue
            if w.flag == 'nr':
                word = w.word
                if word == '蓝忘机' or word == '含光君':
                    word = '蓝湛'
                elif word == '魏无羡' or word == '夷陵老祖':
                    word = '魏婴'
                elif word == '江晚吟' or word == '江宗主':
                    word = '江澄'
                elif word == '泽芜君' or word == '蓝涣':
                    word = '蓝曦臣'
                elif word == '孟瑶' or word == '金宗主' or word == '敛芳尊':
                    word = '金光瑶'
                elif word == '宋子琛' or word == '宋道长' or word == '宋山风':
                    word = '宋岚'
                elif word == '小瞎子':
                    word = '阿箐'
                elif word == '赤锋尊' or word == '聂宗主' or word == '聂明':
                    word = '聂明玦'

                line_name_list[-1].append(word)
                if not word_dict.__contains__(word):
                    word_dict[word] = 0
                word_dict[word] = word_dict[word] + 1

print('word_dict is generated successfully')

words = list(word_dict.items())

cloud = WordCloud()
cloud = cloud.add('', words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
cloud = cloud.set_global_opts(title_opts=opts.TitleOpts(title="魔道祖师小说人物统计"))

page = Page(layout=Page.SimplePageLayout)
page.add(
    cloud
)
page.render("hw2-2-1.html")

# --- 第2步：用字典统计人名“共现”数量（relation_dict）
relation_dict = {}

# 只统计出现次数达到限制数的人名
name_cnt_limit = 100

for line_name in line_name_list:
    for name1 in line_name:
        if word_dict[name1] < name_cnt_limit:
            continue
        # 判断该人物name1是否在字典中
        if name1 not in relation_dict.keys():
            relation_dict[name1] = {}

        # 统计name1与本段的所有人名（除了name1自身）的共现数量
        for name2 in line_name:
            if name2 == name1 or word_dict[name2] < name_cnt_limit:
                continue

            if name2 in relation_dict[name1].keys():
                relation_dict[name1][name2] = relation_dict[name1][name2] + 1
            else:
                relation_dict[name1][name2] = 1

print("共现统计完成，仅统计出现次数达到",
      name_cnt_limit,
      "及以上的人物")

# --- 第3步：输出统计结果
# 字典转成列表，按出现次数排序
item_list = list(word_dict.items())
item_list.sort(key=lambda x: x[1], reverse=True)

# 导出节点文件
node_file = open(node_file_name, 'w')
# 节点文件，格式：Name, Weight -> 人名,出现次数
node_file.write('Name, Weight, Category\n')
node_cnt = 0  # 累计写入文件的节点数量
for name, cnt in item_list:
    if cnt >= name_cnt_limit:  # 只输出出现较多的人物
        cat = category[name] if name in category.keys() else '其他'
        node_file.write(name + ', ' + str(cnt) + ', ' + cat + '\n')
        node_cnt = node_cnt + 1
node_file.close()
print('人物数量：' + str(node_cnt))
print('已写入文件：' + node_file_name)

# 导出连接文件
# 共现数可以看做是连接的权重，只导出权重达到限制数的连接
link_cnt_limit = 10
link_list = []
print('只导出数量达到' + str(link_cnt_limit) + '及以上的连接')
for key1 in relation_dict.keys():
    for key2 in relation_dict[key1].keys():
        if relation_dict[key1][key2] > link_cnt_limit:
            if key2 > key1:
                assert (relation_dict[key2][key1] == relation_dict[key1][key2])
                continue
            link_list.append((key1, key2, relation_dict[key1][key2]))
link_list = sorted(link_list, key=lambda x: x[2], reverse=True)

link_file = open(link_file_name, 'w')
# 连接文件，格式：Source, Target, Weight -> 人名1,人名2,共现数量
link_file.write('Source, Target, Weight\n')
link_cnt = 0  # 累计写入文件的连接数量
for item in link_list:
    name1 = item[0]
    name2 = item[1]
    link = item[2]
    link_file.write(name1 + ', ' + name2 + ', ' + str(link) + '\n')
    link_cnt = link_cnt + 1
link_file.close()
print('连接数量：' + str(link_cnt))
print('已写入文件：' + link_file_name)
