# 这个代码用于获取 cookies 并保存到 ./data/my_cookies.json

from selenium import webdriver
import json
import os
driver = webdriver.Chrome()
# 访问贴吧
driver.get('https://tieba.baidu.com/')
# 提示用户手动登录
print("请手动登录到网站...")
input("登录完成后按回车键继续...")

# 获取 cookies
cookies = driver.get_cookies()
# 创建文件夹（如果不存在）
if not os.path.exists('./data'):
    os.makedirs('./data')
if not os.path.exists('./outputs'):
    os.makedirs('./outputs')
# 保存 cookies 到文件
with open('./data/my_cookies.json', 'w') as f:
    json.dump(cookies, f)
driver.quit()
print("Cookies已保存到./data/my_cookies.json")
