from pyecharts import options as opts
from pyecharts.charts import Page
from pyecharts.charts import Graph

node_file_name = './output/魔道祖师-人物节点-分类.csv'
link_file_name = './output/魔道祖师-人物连接.csv'
out_file_name = './hw2-2-2.html'

# --- 第1步：从文件读入节点和连接信息
node_file = open(node_file_name, 'r', encoding='utf-8')
node_line_list = node_file.readlines()
node_file.close()
del node_line_list[0]  # 删除标题行

link_file = open(link_file_name, 'r', encoding='utf-8')
link_line_list = link_file.readlines()
link_file.close()
del link_line_list[0]  # 删除标题行

# --- 第2步：解析读入的信息，存入列表
# 类别列表，用于给节点分成不同系列，会自动用不同颜色表示
categories = [
    {'name': '云梦江氏'},
    {'name': '姑苏蓝氏'},
    {'name': '兰陵金氏'},
    {'name': '岐山温氏'},
    {'name': '清河聂氏'},
    {'name': '其他'}
]
id = {}
index = 0
for item in categories:
    id[item['name']] = index
    index += 1

node_in_graph = []
for one_line in node_line_list:
    one_line = one_line.strip('\n')
    one_line_list = one_line.split(',')
    node_in_graph.append(opts.GraphNode(
            name=one_line_list[0].strip(),
            value=int(one_line_list[1]),
            symbol_size=int(float(one_line_list[1]) ** 0.5),  # 节点的尺寸，可调
            category=id[one_line_list[2].strip()]))  # 类别
link_in_graph = []
for one_line in link_line_list:
    one_line = one_line.strip('\n')
    one_line_list = one_line.split(',')
    link_in_graph.append(opts.GraphLink(
        source=one_line_list[0].strip(),
        target=one_line_list[1].strip(),
        value=int(one_line_list[2])/100))

# --- 第3步：画图
c = Graph()
c.add("",
      node_in_graph,
      link_in_graph,
      edge_length=[10, 50],
      repulsion=5000,
      categories=categories,
      # 增加连线弧度
      # linestyle_opts=opts.LineStyleOpts(curve=0.2),
      layout="force",  # "force"-力引导布局，"circular"-环形布局
      )
c.set_global_opts(title_opts=opts.TitleOpts(title="魔道祖师人物关系图"))
page = Page(layout=Page.SimplePageLayout)
page.add(c)
c.render(out_file_name)
