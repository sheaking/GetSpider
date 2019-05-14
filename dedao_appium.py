import time
#等待元素控件
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium import webdriver


#
desired_caps = {
  "platformName": "Android",
  "platformVersion": "4.4.2",
  "deviceName": "127.0.0.1:62026",
  "appPackage": "com.luojilab.player",
  "appActivity": "com.luojilab.business.welcome.SplashActivity",
  "noReset": True,
  "unicodeKeyboard": True,
  "resetKeyboard": True
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
wait = WebDriverWait(driver, 10)


def get_size(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x,y)

def handle_dedao(driver):
    # 去除更新按钮
    try:
        if wait.until(lambda x: x.find_element_by_xpath("//android.widget.Button[@resource-id='com.luojilab.player:id/button2']")):
            driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.luojilab.player:id/button2']").click()
    except:
        pass
    # 点击已购买按钮
    if wait.until(lambda x: x.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.luojilab.player:id/threeImageView']")):
        driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.luojilab.player:id/threeImageView']").click()
    # 点击已购买栏
    if wait.until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.luojilab.player:id/tv_sort_latest_purchase']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.luojilab.player:id/tv_sort_latest_purchase']").click()


    # 点击去除×
    try:
        if WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath("//android.widget.Button[@resource-id='com.luojilab.player:id/closeButton']")):
            driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.luojilab.player:id/closeButton']").click()
    except:
        pass

    # 975   195
    l = get_size(driver)
    x1 = int(l[0]*0.5)
    y1 = int(l[0]*0.75)
    y2 = int(l[0]*0.25)

    #
    title_list = []

    #进行栏目的滚动
    count = 0
    while True:
        if count == 0:
            temp = driver.page_source
        elif temp != driver.page_source :
            temp = driver.page_source
        else:
            break
        time.sleep(0.5)
        count += 1
        # 得到开始滚动的元素
        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[3]")):
            origin_el = driver.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[3]")
        # 得到滚动结束的元素
        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]")):
            destination_el = driver.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]")

        # 得到当前页面的栏目框架
        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']")):
            frame_el = driver.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']")

            token = 0
            for index,item in enumerate(frame_el.find_elements_by_class_name("android.widget.RelativeLayout")):
                # 如果为0,2,4，即外层的RelativeLayout
                if index % 2 == 0:
                    print("外层RelativeLayout")
                    inner_layout = item.find_element_by_class_name("android.widget.RelativeLayout")

                    try:
                        if inner_layout.find_element_by_class_name("android.widget.TextView").get_attribute("text") == "电子书":
                            token = 1
                    except:
                        pass

                    try:
                        #判断是否能找到，找不到抛异常
                        item.find_element_by_class_name("android.widget.ImageView")

                        if token == 0:
                            # 如果到这里，说明即不是电子书，有。。。
                            linear_layout = item.find_element_by_class_name("android.widget.LinearLayout")

                            for i in linear_layout.find_elements_by_class_name("android.widget.TextView"):
                                time.sleep(0.5)
                                title_token = i.get_attribute('text')
                                print(title_token)
                                # 如果token没有在列表中，就点击访问
                                if title_token not in title_list:
                                    # dosth

                                    # 添加标记
                                    title_list.append(title_token)
                                    print(title_list)
                                    item.click()
                                    time.sleep(2)
                                    driver.back()
                                break
                        # 有...，但是是电子书
                        else:
                            token = 0
                    except:
                        pass



        # driver.swipe(x1,y1,x1,y2,500)
        driver.scroll(origin_el,destination_el,500)


        # if WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]")):
        #     driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]").click()

if __name__ == '__main__':
    handle_dedao(driver)
