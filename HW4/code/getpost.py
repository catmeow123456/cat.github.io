from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time
import os


def get_data(table_element):
    try:
        row = []
        row.append(table_element.text)
        row.append(table_element.get_attribute('href'))
        return row
    except Exception as e:
        print(e)
        return []


def get_post():
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
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-javascript')
    driver = webdriver.Chrome(options=options)

    start = 0
    end = 10000
    for id in range(start, end, 50):
        driver.get(f"https://tieba.baidu.com/f?kw=%E5%BC%B1%E6%99%BA&fr=index/&ie=utf-8&pn={id}")
        time.sleep(1)
        content = driver.find_elements(By.XPATH, '//*[@id="thread_list"]//li/div/div[2]/div[1]/div[1]/a')
        if not content:
            driver.quit()
            print('请检查是否成功打开网页，可能手动旋转图片通过验证')
            return

        if not os.path.exists('./outputs'):
            os.makedirs('./outputs')
        with open('./outputs/post.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for table in content:
                row = get_data(table)
                if not row:
                    continue
                writer.writerow(row)
    driver.quit()


get_post()
