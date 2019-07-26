from appium_refactor.handle.login_handle import LoginHandle
from appium_refactor.handle.overview_handle import OverviewHandle
import os
class OverviewBusiness:
	def __init__(self,i):
		# self.login_handle = LoginHandle(i)
		self.overview_handle = OverviewHandle(i)


	def go_purchase_page(self):
		print('go_purchase_page------------------------当前进程是----------------------：', os.getpid())
		# import time
		# time.sleep(5)
		self.overview_handle.click_cancel_update()
		self.overview_handle.click_purchased()

	def go_crawl_column_and_article(self):
		#点击第一个栏目
		self.overview_handle.swipe_and_click('column')
		#循环点击文章

	# def login_pass(self):
	# 	self.login_handle.send_username('18513199586')
	# 	self.login_handle.send_password('111111')
	# 	self.login_handle.click_login()
	#
	# def login_user_error(self):
	# 	self.login_handle.send_username('18513199587')
	# 	self.login_handle.send_password('111111')
	# 	self.login_handle.click_login()
	# 	user_flag = self.login_handle.get_fail_tost('帐号未注册')
	# 	if user_flag:
	# 		return True
	# 	else:
	# 		return False
	#
	# def login_password_error(self):
	# 	self.login_handle.send_username('18513199586')
	# 	self.login_handle.send_password('111112')
	# 	self.login_handle.click_login()
	# 	user_flag = self.login_handle.get_fail_tost('登陆密码错误')
	# 	if user_flag:
	# 		return True
	# 	else:
	# 		return False