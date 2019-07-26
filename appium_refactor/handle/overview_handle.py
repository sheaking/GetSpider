# coding=utf-8
from appium_refactor.page.overview_page import OverviewPage
from appium_refactor.page.login_page import LoginPage
import time

class OverviewHandle:
    def __init__(self, i):
        # self.login_page = LoginPage(i)
        self.overview_page = OverviewPage(i)







    def click_cancel_update(self):
        self.overview_page.get_cancel_update().click()
    def click_update(self):
        self.overview_page.get_update().click()
    def click_purchased(self):
        self.overview_page.get_purchased().click()



    def click_recent_learn(self):
        self.overview_page.get_recent_learn().click()
    def click_recent_purchase(self):
        self.overview_page.get_recent_purchase().click()
    def click_course(self):
        self.overview_page.get_course().click()
    def click_column_group(self):
        self.overview_page.get_column_group().click()

    def click_first_column_name(self):
        self.overview_page.get_column_name()[0].click()




    def click_recent_learn2(self):
        self.overview_page.get_recent_learn2().click()
    def click_recent_purchase2(self):
        self.overview_page.get_recent_purchase2().click()
    def click_category_group(self):
        self.overview_page.get_category_group().click()
    def click_column_group2(self):
        self.overview_page.get_column_group2().click()



    def click_finished(self):
        self.overview_page.get_finished().click()
    def click_sort(self):
        self.overview_page.get_sort().click()
    def click_article_group(self):
        self.overview_page.get_article_group().click()



    def click_column(self, no_crawl_column):
        column_names = self.overview_page.get_column_name()

        for column_name in column_names:
            # 这里必需try一下
            try:
                if column_name.get_attribute('text') not in no_crawl_column:
                    no_crawl_column.append(column_name.get_attribute('text'))
                    column_name.click()

                    self.swipe_and_click('article')

                    self.driver_back()
                    self.click_column(no_crawl_column)
            except:
                pass

    def swipe_and_click(self, *args):
        no_crawl_article = []
        no_crawl_column = []
        while True:
            temp = self.get_page_source()
            if args[0] == 'article':
                self.click_article(no_crawl_article)
                names = self.overview_page.get_article_name()
            else:
                self.click_column(no_crawl_column)
                names = self.overview_page.get_column_name()

            if len(names) > 2:
                origin_el = names[1]
                destination_el = names[len(names) - 2]
                self.overview_page.get_driver().drag_and_drop(destination_el, origin_el)

            if temp == self.get_page_source():
                # with open('token.txt', 'wb') as f:
                #     pickle.dump(crawled_article, f)
                break

    def click_article(self, no_crawl_article):
        article_names = self.overview_page.get_article_name()

        for article_name in article_names:
            # 这里必需try一下
            try:
                if article_name.get_attribute('text') not in no_crawl_article:
                    no_crawl_article.append(article_name.get_attribute('text'))
                    article_name.click()
                    time.sleep(1)
                    self.swipe_article()

                    self.driver_back()
                    self.click_article(no_crawl_article)
            except:
                pass

    def swipe_article(self):
        l = self.overview_page.get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)

        n = 0
        while True:
            driver = self.overview_page.get_driver()
            temp = self.get_page_source()
            driver.swipe(x1, y1, x1, y2)
            time.sleep(0.2)
            # if temp == driver.page_source and '点击加载留言' in driver.page_source:
            if temp == driver.page_source:
                if n > 3:
                    break
                n += 1




    def get_page_source(self):
        return self.overview_page.get_driver().page_source


    def driver_back(self):
        self.overview_page.get_driver().back()
