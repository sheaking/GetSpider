# -*- coding: utf-8 -*-
import time
#等待元素控件
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from handle_mysql import MySQL
import pickle
import os

desired_caps = {
  "platformName": "Android",
  "platformVersion": "7.1.2",
  "deviceName": "127.0.0.1:62028",
  "appPackage": "com.luojilab.player",
  "appActivity": "com.luojilab.business.welcome.SplashActivity",
  "noReset": True,
  # "unicodeKeyboard": True, # 需要输入时用这个
  # "resetKeyboard": True,  # 还原输入法
  "automationName": "UiAutomator2"
}

# 本地的appium服务器
server = 'http://localhost:4723/wd/hub'
driver = webdriver.Remote(server, desired_caps)
wait = WebDriverWait(driver, 10)

def get_size(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x,y)

def handle_dedao(driver):
    try:
        # 去除更新按钮，如果没找到更新按钮，就抛异常了，然后pass
        if wait.until(lambda x: x.find_element_by_xpath("//android.widget.Button[@resource-id='com.luojilab.player:id/button2']")):
            driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.luojilab.player:id/button2']").click()
    except:
        pass
    # 点击已购买按钮
    # if wait.until(lambda x: x.find_element_by_id("//android.widget.ImageView[@resource-id='com.luojilab.player:id/threeImageView']")):
    if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/threeImageView")):
        driver.find_element_by_id("com.luojilab.player:id/threeImageView").click()

    if wait.until(lambda x: x.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]")):
        driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]").click()


    # 做爬取记录，爬取过的文章不再爬取
    if os.path.exists('token.txt'):
        with open('token.txt','rb') as f:
            crawled_article = pickle.load(f)
    else:
        crawled_article = []
    print(crawled_article)

    while True:
        # 必须用递归，不然有问题
        crawl_column(driver, crawled_article)
        print(crawled_article)

        # 拖动前临时变量
        temp = driver.page_source

        # 拖动
        if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
        # if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_flat_list")):
            rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
            # rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_flat_list")
            articles = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")

            origin_el = articles[1]
            destination_el = articles[len(articles) - 2]
            driver.drag_and_drop(destination_el, origin_el)

        if temp == driver.page_source:
            with open('token.txt', 'wb') as f:
                pickle.dump(crawled_article, f)
            break



def crawl_column(driver, crawled_article):
    # if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_flat_list")):
    if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
        # rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_flat_list")
        rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
        articles = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")
        for article in articles:
            try:
                title = article.find_element_by_id("com.luojilab.player:id/tv_title").get_attribute("text")
                if title not in crawled_article:
                    # 点击进去爬取
                    article.click()

                    # 进行文章爬取
                    crawl_article(driver)
                    # time.sleep(3)

                    driver.back()
                    crawled_article.append(title)
                    with open('token.txt', 'wb') as f:
                        pickle.dump(crawled_article, f)
                    crawl_column(driver, crawled_article)
            except:
                pass

def crawl_article(driver):
    l = get_size(driver)
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.75)
    y2 = int(l[1] * 0.25)
    while True:
        temp = driver.page_source
        driver.swipe(x1, y1, x1, y2)
        time.sleep(0.2)
        if temp == driver.page_source:
            break



if __name__ == '__main__':
    mysql = MySQL()
    try:
        # mysql.get_connection()
        handle_dedao(driver)
    finally:
        pass
        # mysql.close_connection()
