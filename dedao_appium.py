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


    # 点击已购买栏
    try:
        if wait.until(lambda x: x.find_element_by_xpath("//android.widget.Button[@resource-id='com.luojilab.player:id/closeButton']")):
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

        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[3]")):
            origin_el = driver.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[3]")

        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]")):
            destination_el = driver.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]")

        # 进行点击栏目处理
        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']")):
            frame_el = driver.find_element_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']")
            print(type(frame_el))

            for index,item in enumerate(frame_el.find_elements_by_class_name("android.widget.RelativeLayout")):
                print(type(item))

                try:
                    # 把最里面的RelativeLayout也访问到了
                    # 最里面的就会抛出异常
                    # 这里是外层的RelativeLayout，外层的可能没有ImageView
                    try:
                        #如果有，就不break，没有就break出去
                        item.find_element_by_class_name("android.widget.ImageView")
                    except:
                        continue

                    linear_layout = item.find_element_by_class_name("android.widget.LinearLayout")



                    for i in linear_layout.find_elements_by_class_name("android.widget.TextView"):
                        time.sleep(0.5)
                        title_token = i.get_attribute('text')
                        print(title_token)
                        #如果token没有在列表中，就点击访问
                        if title_token not in title_list:
                            #dosth

                            #添加标记
                            title_list.append(title_token)
                            print(title_list)
                            item.click()
                            time.sleep(2)
                            driver.back()
                        break

                except:
                    # 说明是里层的RelativeLayout
                    try:
                        # 过滤电子书栏目,需要先访问里面的，再访问外面的RelativeLayout，这里暂时没法解决，就通过点进去看看能不能解决，把判断条件放到点击后的里面
                        if item.find_element_by_class_name("android.widget.TextView").get_attribute("text") == '电子书':
                            break
                    except:
                        pass




            # for item in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"android.widget.RelativeLayout"),)):
            #     linear_layout = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"android.widget.RelativeLayout"),item))
            #     for i in

        # driver.swipe(x1,y1,x1,y2,500)
        driver.scroll(origin_el,destination_el,500)


        # if WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]")):
        #     driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.luojilab.player:id/rv_content']/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]").click()

if __name__ == '__main__':
    handle_dedao(driver)
