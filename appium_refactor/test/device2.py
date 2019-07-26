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
  "deviceName": "127.0.0.1:62029",
  # "platformVersion": "7.0",
  # "deviceName": "59428cdc",
  "appPackage": "com.luojilab.player",
  "appActivity": "com.luojilab.business.welcome.SplashActivity",
  "noReset": True,
  "systemPort": 8301,
  # "unicodeKeyboard": True, # 需要输入时用这个
  # "resetKeyboard": True,  # 还原输入法
  "automationName": "UiAutomator2"
}


# 本地的appium服务器
server = 'http://localhost:4723/wd/hub'
driver = webdriver.Remote(server, desired_caps)
wait = WebDriverWait(driver, 10)

try:
    # 去除更新按钮，如果没找到更新按钮，就抛异常了，然后pass
    if wait.until(lambda x: x.find_element_by_xpath(
            "//android.widget.Button[@resource-id='com.luojilab.player:id/button2']")):
        driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.luojilab.player:id/button2']").click()
except:
    pass
# 点击已购买按钮
# if wait.until(lambda x: x.find_element_by_id("//android.widget.ImageView[@resource-id='com.luojilab.player:id/threeImageView']")):
if wait.until(lambda x: x.find_element_by_id("com.luojilab.player:id/threeImageView")):
    driver.find_element_by_id("com.luojilab.player:id/threeImageView1").click()

# time.sleep(10)
# while True:
#   print('---------'*3)
#   print(driver.contexts)
#   time.sleep(5)
