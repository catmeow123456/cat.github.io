# 这个代码访问 post.csv 中的每一条帖子的链接，并获取帖子的内容
# 将每个帖子中的内容保存到 outputs 文件夹中，文件名为 message{帖子编号}.txt。

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time
import json
import os


def get_message():
    options = Options()
    driver = webdriver.Chrome(options=options)
    # 访问贴吧
    driver.get('https://tieba.baidu.com/')
    # 在这一步弹出的浏览器中可能会出现验证码，需要在 10 秒内两次旋转图片到正确角度通过验证。
    time.sleep(10)

    # 加载 cookies （模拟用户登陆）
    with open('./data/my_cookies.json', 'r') as f:
        cookies_data = json.load(f)
    for cookie in cookies_data:
        driver.add_cookie(cookie)
    driver.refresh()

    # 添加 cookie 登陆之后可能会出现验证码，需要在 5 秒内旋转图片到正确角度通过验证。
    time.sleep(5)

    # 读取 post.csv，获取每个帖子的标题和对应的链接
    with open('./outputs/post.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    cnt = 0

    # 遍历每个帖子
    for row in rows:
        cnt = cnt + 1
        # 输出进度，因为很慢……
        print('进度：', cnt, '/', len(rows))
        url = row[1]
        # 确保链接的格式是正确的
        assert url.startswith("https://tieba.baidu.com/p/")
        # 将链接中帖子编号部分提取出来，作为文件名，并创建相应的文件
        filename = url.removeprefix('https://tieba.baidu.com/p/')
        filename = f'./outputs/message{filename}.txt'
        if os.path.exists(filename):
            print(f'{filename} already exists')
            continue
        print(f'writing to {filename}...')
        # 打开帖子链接准备爬取内容
        driver.get(url)
        time.sleep(1)
        # 检查该帖子内容是否被隐藏或者删除，或者是否出现其他错误而无法访问
        error_text = driver.find_elements(By.ID, 'errorText')

        if error_text:
            # 通过寻找 CLASS_NAME='main-title' 的元素来判断错误类型
            info = error_text[0].find_element(By.CLASS_NAME, 'main-title')
            if info.text.strip() == '抱歉，您访问的贴子被隐藏，暂时无法访问。':
                print('抱歉，您访问的贴子被隐藏，暂时无法访问。')
                with open(filename, 'w', newline='', encoding='utf-8') as txtfile:
                    txtfile.write(row[0]+'\n'+'\n')
                    txtfile.write('抱歉，您访问的贴子被隐藏，暂时无法访问。'+'\n')
                continue
            if info.text.strip() == '很抱歉，该贴已被删除 返回首页':
                print('很抱歉，该贴已被删除 返回首页')
                with open(filename, 'w', newline='', encoding='utf-8') as txtfile:
                    txtfile.write(row[0]+'\n'+'\n')
                    txtfile.write('很抱歉，该贴已被删除 返回首页'+'\n')
                continue
            print(info.text)
            raise ValueError('未知错误')
        # 如果没有错误，则可以正常访问帖子。
        # 首先获取帖子的页数，以便后续爬取
        # 通过 XPATH 来寻找元素 //*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[2]
        page_num = driver.find_element(By.XPATH, '//*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[2]')
        print('标题：', row[0], '，共', page_num.text, '页')
        # 先写入标题
        with open(filename, 'w', newline='', encoding='utf-8') as txtfile:
            txtfile.write(row[0]+'\n'+'\n')
        # 逐页爬取帖子内容
        for id in range(1, int(page_num.text)+1):
            # 第 id 页面的链接为 idth_url
            idth_url = url + f'?pn={id}'
            driver.get(idth_url)
            # 每隔 0.5 秒爬取一次
            time.sleep(0.5)
            # 获取帖子内容，通过 CLASS_NAME='j_d_post_content' 来寻找元素
            elems = driver.find_elements(By.CLASS_NAME, 'j_d_post_content')
            if not elems:
                raise ValueError('未找到内容，请检查是否成功打开网页')  # 有可能被验证吗拦截
            # 将内容写入文件
            with open(filename, 'a', newline='', encoding='utf-8') as txtfile:
                for elem in elems:
                    print(elem.text)
                    txtfile.write(elem.text+'\n')
    driver.quit()


get_message()
