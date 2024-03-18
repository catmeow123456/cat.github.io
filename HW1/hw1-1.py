import json
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Page

"""
2200 家人工智能企业\n在省市自治区的分布(2023)
数据来源：https://www.kdocs.cn/l/cbKC87pGFlmP
"""
with open(file="./data/hw1-1-1.json", mode="r") as file:
    res = json.load(file)

range_color = ['#fefefe',
               'yellow',
               'orange',
               'red']

c = (
    Map()
    .add("企业分布百分比(%)", res,
         maptype="china", zoom=1.2, pos_left=100,pos_top=150)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2200 家人工智能企业\n在省市自治区的分布(2023)"),
        visualmap_opts=opts.VisualMapOpts(max_=30,
                                          range_color=range_color,
                                          # split_number=4,
                                          # is_piecewise=True
                                          ),
    )
)
page = Page(layout=Page.SimplePageLayout)
page.add(
    c
)
page.render(path="hw1-1-1.html")


"""
数据来源

2023 GLOBAL ARTIFICIAL INTELLIGENCE INFRASTRUCTURES REPORT
https://www.stimson.org/wp-content/uploads/2023/08/AI-Strategies-2023-Global-AI-Infratructures-Report.pdf

2023 Artificial Intelligence Index Report
https://arxiv.org/ftp/arxiv/papers/2310/2310.03715.pdf
"""

with open(file="./data/hw1-1-2.json", mode="r") as file:
    res = json.load(file)
res0 = res[0] # AI Journal Publications (% of World Total) by Geographic Area, 2010–21
res1 = res[1] # AI Repository Publications by Geographic Area (% of World Total) 2021
res2 = res[2] # Number of Authors of Significant Machine Learning Systems by Country, 2022

c = (
    Map()
    # .add("AI Journal Publication (%)", res0,
    #      maptype="world")
    # .add("AI Repository Publications (%)", res1,
    #      maptype="world")
    .add("Number of Authors of Significant Machine Learning Systems", res2,
         maptype="world")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Number of Authors\nof Significant Machine Learning Systems by Country, 2022\n"),
        visualmap_opts=opts.VisualMapOpts(max_=300,
                                          range_color=range_color,
                                          ),
    )
)
page = Page(layout=Page.SimplePageLayout)
page.add(
    c
)
page.render(path="hw1-1-2.html")