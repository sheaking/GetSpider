# -*- coding: utf-8 -*-
import time
#等待元素控件
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from handle_mysql import MySQL
import pickle
import os
'''
根据数据库去重爬取
'''
desired_caps = {
  "platformName": "Android",
  # "platformVersion": "7.1.2",
  # "deviceName": "127.0.0.1:62028",
  "platformVersion": "7.0",
  "deviceName": "59428cdc",
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
    return (x, y)

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

    # 点击课程
    if wait.until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.luojilab.player:id/tv_course']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.luojilab.player:id/tv_course']").click()

    # 点击课程里面的最新购买
    if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/nearBuyBtn")):
        driver.find_element_by_id("com.luojilab.player:id/nearBuyBtn").click()

    # 得到正在更新列表，不爬取这些正在更新列表
    no_crawl_columns = []
    get_no_crawl_columns(driver, no_crawl_columns, '正在更新')
    # get_no_crawl_columns(driver, no_crawl_columns, '其他')
    # print(no_crawl_columns)

    # 从数据库中取出爬取完毕的栏目，去重
    # def f(x):
    #     return x[0]
    # db_crawled_finished_columns = mysql.select('tb_column', ['column_name'], '1 = 1')
    # db_crawled_finished_columns = mysql.select('column_', ['column_name'], '1 = 1')
    # print(result)
    # if db_crawled_finished_columns:
    #     no_crawl_columns += list(map(f, db_crawled_finished_columns))
    print('去除正在更新中的栏目：', no_crawl_columns)

    # 点击全部列表
    # if wait.until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='全部 133']")):
    if wait.until(lambda x: x.find_element_by_xpath("//android.widget.TextView[contains(@text,'全部')]")):
        driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'全部')]").click()

    #开始大循环栏目列表
    while True:
        # 循环当前页面的栏目列表，并把点击后的栏目列表放到no_crawl_columns中
        crawl_columns_list(driver, no_crawl_columns)
        # print(db_crawled_finished_columns)

        # 拖动前临时变量
        temp = driver.page_source
        # 拖动                                                android.support.v7.widget.RecyclerView
        if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
        # if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_flat_list")):
            rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
            # rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_flat_list")
            columns = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")
            print('当前页面栏目数量：', len(columns))
            origin_el = columns[1]
            destination_el = columns[len(columns) - 2]
            driver.drag_and_drop(destination_el, origin_el)
            print('当前不爬取的栏目：', no_crawl_columns)

        if temp == driver.page_source:
            break

def crawl_columns_list(driver, no_crawl_columns):
    '''
    循环点击当前页面的所有栏目
    :param driver:
    :param no_crawl_columns: 这是点击过的栏目，不循环点击
    :return:
    '''
    if wait.until(lambda x: x.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']")):
        columns = driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']")
        column_list = columns.find_elements_by_id("com.luojilab.player:id/home_newsub_item")
        for column in column_list:
            try:
                column_name = column.find_element_by_id("com.luojilab.player:id/column_name").get_attribute("text")
                if column_name not in no_crawl_columns:
                    # 放到第一行
                    no_crawl_columns.append(column_name)
                    # 点击栏目，通过标题点击！
                    crawled_articles = check_column_over(column_name)
                    if not crawled_articles is None:
                        # 不用点进去就能判断
                        column.find_element_by_id("com.luojilab.player:id/column_name").click()

                        time.sleep(2)

                        # 爬取此栏目所有文章
                        crawl_column(driver, crawled_articles)
                        driver.back()

                    crawl_columns_list(driver, no_crawl_columns)
            except:
                pass


def check_column_over(column_name):
    print('正在爬取栏目：', column_name)
    # 从数据库中取出该栏目爬取完毕的文章，去重
    column = mysql.select('tb_column', ['column_id', 'current_article_num'], 'column_name="%s"' % column_name)
    # print(result)
    # 这篇栏目爬取的文章的名称
    crawled_articles = []
    flag = False

    # 如果数据库中有此栏目
    if column:
        column_id = column[0][0]
        current_article_num = column[0][1]
        # print('当前栏目:', column_id, column_name, current_article_num)

        def f(x):
            return x[0]

        crawled_article_id = mysql.select('article_column', ['article_id'], 'column_id="%s"' % column_id)
        crawled_article_ids = list(map(f, crawled_article_id))
        print('当前栏目id = %s, 栏目名称：%s' % (column_id, column_name), current_article_num, crawled_article_ids)
        print(len(crawled_article_ids), current_article_num)
        # 如果栏目没有被爬取完毕
        if len(crawled_article_ids) < current_article_num:
            for article_id in crawled_article_ids:
                article_name = mysql.select('article', ['article_name'], 'article_id="%s"' % article_id)
                if article_name:
                    article_name = article_name[0][0]
                    crawled_articles.append(article_name)
                    # print(article_name)
        # 如果文章爬取完毕，就返回
        else:
            flag = True

    if flag:
        return
    else:
        print('当前栏目已经爬取文章名：', crawled_articles)
        return crawled_articles



def crawl_column(driver,crawled_articles):
    '''
    爬取栏目所有文章
    进去可能会出现奖章页面
    进去第一篇文章可能不在顶部
    :param driver:
    :param column_name:
    :return:
    '''

    # 从数据库中获取这个栏目已经爬取的文章的标题

    # if os.path.exists('token.txt'):
    #     with open('token.txt','rb') as f:
    #         crawled_article = pickle.load(f)
    # else:
    #     crawled_article = []
    # print(crawled_article)

    # 如果出现完成奖章页面
    time.sleep(3)
    if '如此优秀的你学完了' in driver.page_source:
        driver.back()


    # 向上滑动，去到最顶端
    if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/tv_sort")):
        sort_btn = driver.find_element_by_id("com.luojilab.player:id/tv_sort")
        sort_btn.click()
        time.sleep(3)
        sort_btn.click()
        time.sleep(1)
        # 向上滑动窗口
        l = get_size(driver)
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.9)
        y2 = int(l[1] * 0.5)
        n = 0
        while n < 100:
            temp = driver.page_source
            driver.swipe(x1, y2, x1, y1)
            time.sleep(0.5)
            if temp == driver.page_source:
                break
            n += 1

    # 爬取每一篇文章
    while True:

        crawl_articles(driver, crawled_articles)
        temp = driver.page_source

        # 拖动
        if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
            # if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_flat_list")):
            rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
            # rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_flat_list")
            articles = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")
            if len(articles) == 0:
                # if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
                try:
                    if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_flat_list")):
                        # rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
                        rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_flat_list")
                        articles = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")
                except:
                    # if len(articles) == 0:
                    # if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
                    if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_chapter_list")):
                        # rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
                        rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_chapter_list")
                        articles = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")

            if len(articles) == 0:
                return

            origin_el = articles[1]
            destination_el = articles[len(articles) - 2]
            driver.drag_and_drop(destination_el, origin_el)

        if temp == driver.page_source:
            # with open('token.txt', 'wb') as f:
            #     pickle.dump(crawled_article, f)
            break


def crawl_articles(driver, crawled_articles):
    # if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_flat_list")):
    if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
        # rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_flat_list")
        rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
        articles = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")
        if len(articles) == 0:
            # if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
            try:
                if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_flat_list")):
                    # rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
                    rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_flat_list")
                    articles = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")
            except:
            # if len(articles) == 0:
                # if wait.until(lambda x: x.find_element_by_class_name("android.support.v7.widget.RecyclerView")):
                if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/rv_chapter_list")):
                    # rv_flat_list = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
                    rv_flat_list = driver.find_element_by_id("com.luojilab.player:id/rv_chapter_list")
                    articles = rv_flat_list.find_elements_by_class_name("android.widget.LinearLayout")



        if len(articles) == 0:
            return

        for article in articles:
            try:
                title = article.find_element_by_id("com.luojilab.player:id/tv_title").get_attribute("text")
                if title not in crawled_articles:
                    # 放到第一行
                    crawled_articles.append(title)

                    # 点击进去爬取,最好通过点击标题进入，不然其他方式进不去
                    article.find_element_by_id("com.luojilab.player:id/tv_title").click()
                    time.sleep(3)
                    # 进行文章爬取

                    # crawl_article(driver)
                    driver.back()


                    # with open('token.txt', 'wb') as f:
                    #     pickle.dump(crawled_article, f)
                    crawl_articles(driver, crawled_articles)
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
        if temp == driver.page_source and '点击加载留言' in driver.page_source:
            break
    # db_crawled_unfinished_columns = mysql.select('tb_column', ['column_name'], 'crawl_finished = 0')


def get_no_crawl_columns(driver, no_crawl_columns, target):
    if wait.until(lambda x: x.find_element_by_xpath("//android.view.ViewGroup")):
        view_group = driver.find_element_by_xpath("//android.view.ViewGroup")
        column_tabs = view_group.find_elements_by_class_name("android.widget.TextView")

        for column_tab in column_tabs:
            if target in column_tab.get_attribute("text"):
                column_tab.click()

                while True:
                    temp = driver.page_source

                    column_names = driver.find_elements_by_id("com.luojilab.player:id/column_name")
                    for column_name in column_names:
                        try:
                            no_crawl_columns.append(column_name.get_attribute("text"))
                        except:
                            pass
                    origin_el = column_names[0]
                    destination_el = column_names[len(column_names) - 2]

                    driver.drag_and_drop(destination_el, origin_el)

                    if temp == driver.page_source:
                        break
                print(no_crawl_columns)
                reset_columns(driver)
                break

# 重置column列表
def reset_columns(driver):
    # 重置列表
    driver.back()
    # 点击课程
    if wait.until(lambda x: x.find_element_by_xpath(
            "//android.widget.TextView[@resource-id='com.luojilab.player:id/tv_course']")):
        driver.find_element_by_xpath(
            "//android.widget.TextView[@resource-id='com.luojilab.player:id/tv_course']").click()

    # 点击课程里面的最新购买
    if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/nearBuyBtn")):
        driver.find_element_by_id("com.luojilab.player:id/nearBuyBtn").click()

if __name__ == '__main__':

    mysql = MySQL()
    try:
        mysql.get_connection()
        handle_dedao(driver)
    finally:
        mysql.close_connection()
