import json
from pyecharts import options as opts
from pyecharts.charts import Page
from pyecharts.charts import Bar, Line

res_mathlib3 = {}
res_mathlib4 = {}
res_mathlib3_line_number = {}
res_mathlib4_line_number = {}
x_axis = []

def read_data():
    global res_mathlib3
    global res_mathlib4
    global res_mathlib3_line_number
    global res_mathlib4_line_number
    global x_axis
    with open(file="data/hw1-2.json", mode="r") as file:
        res = json.load(file)
        res_mathlib3 = res["mathlib3"]
        res_mathlib4 = res["mathlib4"]
        res_mathlib3_line_number = res["mathlib3_line_number"]
        res_mathlib4_line_number = res["mathlib4_line_number"]
        x_axis = sorted(set(res_mathlib3.keys()) | set(res_mathlib4.keys()), key=lambda x : int(x))
    for x in x_axis:
        if not res_mathlib3.__contains__(x):
            res_mathlib3[x] = 0
        if not res_mathlib4.__contains__(x):
            res_mathlib4[x] = 0
        if not res_mathlib3_line_number.__contains__(x):
            res_mathlib3_line_number[x] = 0
        if not res_mathlib4_line_number.__contains__(x):
            res_mathlib4_line_number[x] = 0

def overlap_bar_line() -> Bar:
    c = Bar()
    c = c.add_xaxis(x_axis)
    c = c.add_yaxis("mathlib3", [res_mathlib3[key] for key in x_axis])
    c = c.add_yaxis("mathlib4", [res_mathlib4[key] for key in x_axis])
    c = c.extend_axis(
        yaxis=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value} 行"), interval=100000
        )
    )
    c = c.set_global_opts(
        title_opts=opts.TitleOpts(title="mathlib3 与 mathlib4\n仓库 commit 数量和总代码量逐年对比"),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value} commits"), interval=1000
        ),
    )
    l = Line().add_xaxis(x_axis)
    l = l.add_yaxis("mathlib3 代码总行数", [res_mathlib3_line_number[key] for key in x_axis], yaxis_index=1)
    l = l.add_yaxis("mathlib4 代码总行数", [res_mathlib4_line_number[key] for key in x_axis], yaxis_index=1)
    c = c.overlap(l)
    return c

def generate_page():
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        overlap_bar_line()
    )
    page.render("./hw1-2.html")

if __name__ == "__main__":
    read_data()
    generate_page()