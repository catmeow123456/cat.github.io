from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time
import json
import os


def get_message():
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    # options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-javascript')
    driver = webdriver.Chrome(options=options)
    driver.get('https://tieba.baidu.com/')
    # 在这一步弹出的浏览器中可能会出现验证码，需要在 10 秒内两次旋转图片到正确角度通过验证。
    time.sleep(10)
    with open('./data/my_cookies.json', 'r') as f:
        cookies_data = json.load(f)
    for cookie in cookies_data:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)
    # 添加 cookie 登陆之后可能会出现验证码，需要在 5 秒内旋转图片到正确角度通过验证。
    with open('./outputs/post.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    cnt = 0
    for row in rows:
        cnt = cnt + 1
        print('进度：', cnt, '/', len(rows))
        url = row[1]
        assert url.startswith("https://tieba.baidu.com/p/")
        filename = url.removeprefix('https://tieba.baidu.com/p/')
        filename = f'./outputs/message{filename}.txt'
        if os.path.exists(filename):
            print(f'{filename} already exists')
            continue
        print(f'writing to {filename}...')
        driver.get(url)
        # driver.refresh()
        time.sleep(1)
        error_text = driver.find_elements(By.ID, 'errorText')

        if error_text:
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
# //*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[2]
        page_num = driver.find_element(By.XPATH, '//*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[2]')
        print('标题：', row[0], '，共', page_num.text, '页')
        with open(filename, 'w', newline='', encoding='utf-8') as txtfile:
            txtfile.write(row[0]+'\n'+'\n')
        for id in range(1, int(page_num.text)+1):
            idth_url = url + f'?pn={id}'
            driver.get(idth_url)
            time.sleep(0.5)
            elems = driver.find_elements(By.CLASS_NAME, 'j_d_post_content')
            if not elems:
                raise ValueError('未找到内容，请检查是否成功打开网页')  # 有可能被验证吗拦截
            with open(filename, 'a', newline='', encoding='utf-8') as txtfile:
                for elem in elems:
                    print(elem.text)
                    txtfile.write(elem.text+'\n')
    driver.quit()


get_message()
