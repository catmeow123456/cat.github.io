from selenium import webdriver
import json
import os
driver = webdriver.Chrome()
driver.get('https://tieba.baidu.com/')
print("请手动登录到网站...")
input("登录完成后按回车键继续...")
cookies = driver.get_cookies()
if not os.path.exists('./data'):
    os.makedirs('./data')
if not os.path.exists('./outputs'):
    os.makedirs('./outputs')
with open('./data/my_cookies.json', 'w') as f:
    json.dump(cookies, f)
driver.quit()
print("Cookies已保存到./data/my_cookies.json")
