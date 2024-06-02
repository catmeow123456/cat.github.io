# 这个代码的作用是爬取百度贴吧的帖子，将帖子的标题和链接保存到 ./outputs/post.csv 文件中
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time
import os


def get_data(table_element):
    # 当前函数传入的是一个帖子文本块的元素，例如：
    # <a rel="noopener" href="/p/8624969962" title="弱智吧官方水楼！注意！从今天起在其他贴子里水经验将概率封禁" target="_blank" class="j_th_tit ">
    # 弱智吧官方水楼！注意！从今天起在其他贴子里水经验将概率封禁</a>
    try:
        row = []
        # 从帖子文本块的元素中提取“内容”和“链接”信息，将这两个信息放入列表中返回
        row.append(table_element.text)  # 元素内容，就是帖子的标题
        row.append(table_element.get_attribute('href'))  # href 属性就是帖子的链接
        return row
    except Exception as e:
        # 如果出现错误或异常，则将错误信息输出到 terminal 中
        print(e)
        return []


def get_post():
    options = Options()
    driver = webdriver.Chrome(options=options)  # 创建 webdriver 对象

    # 以“弱智吧”为例，网址的格式为
    # f"https://tieba.baidu.com/f?kw=%E5%BC%B1%E6%99%BA&fr=index/&ie=utf-8&pn={id}"
    # 其中 id 为 50 的倍数，百度贴吧一页包含了 50 个帖子，我们可以从 0 到 10000 枚举 所有 50 的倍数来遍历可能的 id。
    start = 0
    end = 10000
    for id in range(start, end, 50):
        # 访问弱智吧（第 id/50+1 页）的信息
        driver.get(f"https://tieba.baidu.com/f?kw=%E5%BC%B1%E6%99%BA&fr=index/&ie=utf-8&pn={id}")
        # 隔一秒钟访问下一个页面
        time.sleep(1)
        # 寻找帖子块所对应的元素
        content = driver.find_elements(By.XPATH, '//*[@id="thread_list"]//li/div/div[2]/div[1]/div[1]/a')
        # 如果没有找到帖子块，可能是因为被检测到是机器人，需要手动旋转图片通过验证
        if not content:
            driver.quit()
            print('请检查是否成功打开网页，可能手动旋转图片通过验证')
            return
        # （如果不存在的话）创建输出文件夹
        if not os.path.exists('./outputs'):
            os.makedirs('./outputs')
        # 将帖子的标题和链接保存到 ./outputs/post.csv 文件中
        with open('./outputs/post.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # 枚举所有的帖子块
            for table in content:
                # 获取标题和链接信息
                row = get_data(table)
                if not row:
                    continue
                # 输出到 csv 文件中
                writer.writerow(row)
    driver.quit()


get_post()
