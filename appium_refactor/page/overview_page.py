#coding=utf-8
from appium_refactor.util.get_by_local import GetByLocal
import time
from appium_refactor.base.base_driver import BaseDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OverviewPage:
	# 获取登录页面所有的页面元素信息
	def __init__(self,i):
		base_driver = BaseDriver()
		self.driver = base_driver.android_driver(i)
		self.get_by_local = GetByLocal(self.driver)
		self.overview_element_section = 'overview_element'
		self.purchase_element_section = 'purchase_element'
		self.course_element_section = 'course_element'
		self.column_element_section = 'column_element'
		print('第 %s 个driver, driver: %s', (i, self.driver))

	def get_size(self):
		x = self.get_driver().get_window_size()['width']
		y = self.get_driver().get_window_size()['height']
		return (x, y)

	def get_driver(self):
		return self.driver

	def get_cancel_update(self):
		'''
		获取用户名元素信息
		'''
		import os
		# print('---------当前进程是----------', os.getpid(), self.get_by_local)
		# print('---------当前进程是----------,元素是',os.getpid(),self.get_by_local, self.get_by_local.get_element('cancel_update',self.overview_element_section), self.driver.capabilities)
		return self.get_by_local.get_element('cancel_update',self.overview_element_section)[0]


	def get_update(self):
		'''
		获取密码元素信息
		'''
		return self.get_by_local.get_element('update',self.overview_element_section)[0]

	def get_purchased(self):
		'''
		获取登陆按钮元素信息
		'''
		return self.get_by_local.get_element('purchased',self.overview_element_section)[0]





	def get_recent_learn(self):
		return self.get_by_local.get_element('recent_learn',self.purchase_element_section)[0]
	def get_recent_purchase(self):
		return self.get_by_local.get_element('recent_purchase', self.purchase_element_section)[0]
	def get_course(self):
		return self.get_by_local.get_element('course', self.purchase_element_section)[0]
	def get_column_group(self):
		return self.get_by_local.get_element('column_group', self.purchase_element_section)[0]
	def get_column_name(self):
		return self.get_by_local.get_element('column_name', self.purchase_element_section)






	def get_recent_learn2(self):
		return self.get_by_local.get_element('recent_learn', self.course_element_section)[0]
	def get_recent_purchase2(self):
		return self.get_by_local.get_element('recent_purchase', self.course_element_section)[0]
	def get_category_group(self):
		return self.get_by_local.get_element('category_group', self.course_element_section)[0]
	def get_column_group2(self):
		return self.get_by_local.get_element('column_group', self.course_element_section)[0]





	def get_finished(self):
		return self.get_by_local.get_element('finished', self.column_element_section)[0]
	def get_sort(self):
		return self.get_by_local.get_element('sort', self.column_element_section)[0]
	def get_article_group(self):
		return self.get_by_local.get_element('article_group', self.column_element_section)[0]
	def get_article_name(self):
		return self.get_by_local.get_element('article_name', self.column_element_section)

