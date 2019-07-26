#coding=utf-8
from appium_refactor.util.read_init import ReadIni
from selenium.webdriver.support.ui import WebDriverWait
import os
class GetByLocal:
	def __init__(self,driver):
		self.driver = driver
		self.wait = WebDriverWait(driver, 10)
	def get_element(self,key,section):
		read_ini = ReadIni()
		local = read_ini.get_value(key,section)
		# print('local'*5, local)
		if local != None:
			by = local.split('>')[0]
			local_by = local.split('>')[1]
			# print('localby'*5, local_by)
			try:
				if by == 'id':
					if self.wait.until(lambda x: x.find_elements_by_id(local_by)):
						return self.driver.find_elements_by_id(local_by)
				elif by == 'className':
					if self.wait.until(lambda x: x.find_elements_by_class_name(local_by)):
						return self.driver.find_elements_by_class_name(local_by)
				else:

					print('1111当前进程是：%s,当前driver是：%s，当前查找元素为：%s, caps：%s'% (os.getpid(), self.driver, local_by, self.driver.capabilities))
					if self.wait.until(lambda x: x.find_elements_by_xpath(local_by)):
						print('2222当前进程是：%s,当前driver是：%s，当前查找元素为：%s, caps：%s'% (os.getpid(), self.driver, local_by, self.driver.capabilities))
						return self.driver.find_elements_by_xpath(local_by)
			except:
				print('3333当前进程是：%s,当前driver是：%s，当前查找元素为：%s, caps：%s'% (os.getpid(), self.driver, local_by, self.driver.capabilities))
				# print(self.driver.capabilities)
				# 保存截图
				# 是同一个driver
				self.driver.save_screenshot("../jpg/test03.png")
				self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.luojilab.player:id/tv_course']").click()
				return None
		else:
			return None


