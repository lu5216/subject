import time
import random
import pandas as pd
from PySide2.QtWidgets import QMessageBox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine, types

# 随机sleep时间（2-3秒内）
def sleep_time():
    sleepTime = random.random()*3
    while sleepTime<2:
        sleepTime = random.random()*3
    return sleepTime


# 北证A股
def getdata_tocsv(page, dt):
    # 浏览器驱动位置
    ChromeDriver = "./util/chromedriver.exe"
    service = Service(executable_path=ChromeDriver)
    # 浏览器位置
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = r"D:\\chrome\\GoogleChromePortable64\App\\Chrome-bin\\chrome.exe"
    browser = webdriver.Chrome(service=service,options=options)
    # 股票网站
    url = 'https://quote.eastmoney.com/center/gridlist.html'
    browser.get(url)
    time.sleep(sleep_time())

    # 获取单个页面的股票信息
    data_dt = {'代码':[], '名称':[]}

    def get_data():
        list2 = browser.find_elements(By.XPATH, '//*[@id="table_wrapper-table"]/tbody/tr/td[2]')
        list3 = browser.find_elements(By.XPATH, '//*[@id="table_wrapper-table"]/tbody/tr/td[3]')
        for i2 in list2: data_dt['代码'].append(i2.text)
        for i3 in list3: data_dt['名称'].append(i3.text)

    # 定位class="paginate_page"下的所有<a>标签
    pn_list = browser.find_elements(By.CSS_SELECTOR, '#main-table_paginate > span.paginate_page > a')
    pn = int(pn_list[-1].text)  # 选取最后一个<a>标签的文本，即总页数
    if pn < page:
        QMessageBox.about(None,"错误",f"输入的页数大于最大页数{pn}")
    else:
        for p in range(page):
            get_data()
            # 下一页按钮
            a_btn = browser.find_element(By.CSS_SELECTOR, '#main-table_paginate > a.next.paginate_button')
            a_btn.click()   # 模拟点击
            time.sleep(sleep_time())
        browser.quit()      # 关闭浏览器窗口

        data1 = pd.DataFrame(data_dt)
        data1.to_csv(f'CsvFile/{dt}.csv', index=False)
        QMessageBox.about(None, "成功", "数据爬取成功！！！")




def getcsv_todatabase(dt):
    data = pd.read_csv(f'CsvFile/{dt}.csv', converters={'股票代码': str})
    data.to_csv(f'CsvFile/{dt}.csv', index=False)

    sql = f'{dt}_stock'
    con = create_engine('mysql+pymysql://root:123456@localhost:3306/stock?charset=utf8')
    data.to_sql(sql, con=con, index_label=['id'], if_exists='replace', 
                dtype={
                    '序号': types.BigInteger(),
                    '代码': types.VARCHAR(100),
                    '名称': types.VARCHAR(100),
                       })
    QMessageBox.about(None, "成功","数据成功存入数据库！！！")







# if __name__ == "__main__":
#     # 1、爬取数据，并存储到csv
#     getdata_tocsv()
#     # 2、读取csv，并存储到数据库
#     getcsv_todatabase()

