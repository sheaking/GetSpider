#coding=utf-8
import time
from appium import webdriver
from appium_refactor.util.write_user_command import WriteUserCommand
from appium_refactor.util.port import Port
class BaseDriver:
	def android_driver(self,i):
		print("this is android_driver:",i)
		#devices_name adb devices
		#port
		port = Port()
		port_list = port.create_port_list(8200, [1])
		systemPort = port_list[0] + int(i)
		write_file = WriteUserCommand()
		devices = write_file.get_value('user_info_'+str(i),'deviceName')
		port = write_file.get_value('user_info_'+str(i),'port')
		if '127.0.0.1' in str(devices):
			platformVersion = '7.1.2'
		else:
			platformVersion = '7.0'

		capabilities = {
			"platformName": "Android",
			"platformVersion":platformVersion,
			"deviceName": devices,
		  # "app": "E:\\PythonAppium\\AutoTestAppium\\apps\\mukewang.apk",
		  # "appWaitActivity":"cn.com.open.mooc.user.login.MCLoginActivity",
			"udid": devices,
			# "app":'D:\\apk\\apk\\201904161821564778822679.apk',
			# "appWaitActivity": "com.luojilab.business.welcome.SplashActivity",
			"appPackage": "com.luojilab.player",
			"appActivity": "com.luojilab.business.welcome.SplashActivity",
			"systemPort": systemPort,

			"noReset":"true",
  		  # "automationName": "Espresso"
  			"automationName": "UiAutomator2"
		  # "appPackage":"cn.com.open.mooc"
		  #"newCommandTimeout":'180'
		}
		driver = webdriver.Remote("http://127.0.0.1:"+str(port)+"/wd/hub",capabilities)
		print('driver_info：', devices, port)
		# print(capabilities)

		# if '127.0.0.1:62028' == devices:
		# 	time.sleep(20)
		time.sleep(5)
		return driver
