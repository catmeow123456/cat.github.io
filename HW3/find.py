from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import csv
import time
import os
with open('./data/my_cookies.json', 'r') as f:
    cookies_data = json.load(f)
driver = webdriver.Chrome()
driver.get("https://www.bilibili.com/")
for cookie in cookies_data:
    driver.add_cookie(cookie)
time.sleep(1)
driver.refresh()
driver.get('https://member.bilibili.com/platform/home')
time.sleep(0.5)
content = driver.find_elements(By.CLASS_NAME, 'data-wrp')


def table_to_2d_list(table_element):
    rows = []
    list = table_element.find_elements(By.CLASS_NAME, 'data-card-detail')
    for item in list:
        s = item.text.split('\n')
        while (len(s) < 5):
            s.append('')
        rows.append(s)
    return rows


if not os.path.exists('./outputs'):
    os.makedirs('./outputs')
with open('./outputs/output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for table in content:
        print(table)
        table_data = table_to_2d_list(table)
        for row in table_data:
            writer.writerow(row)
driver.quit()
