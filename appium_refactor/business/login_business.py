#coding=utf-8
from appium_refactor.handle.login_handle import LoginHandle
class LoginBusiness:
	def __init__(self,i):
		self.login_handle = LoginHandle(i)

	def login_pass(self):
		self.login_handle.send_username('18513199586')
		self.login_handle.send_password('111111')
		self.login_handle.click_login()

	def login_user_error(self):
		self.login_handle.send_username('18513199587')
		self.login_handle.send_password('111111')
		self.login_handle.click_login()
		user_flag = self.login_handle.get_fail_tost('帐号未注册')
		if user_flag:
			return True
		else:
			return False
			
	def login_password_error(self):
		self.login_handle.send_username('18513199586')
		self.login_handle.send_password('111112')
		self.login_handle.click_login()
		user_flag = self.login_handle.get_fail_tost('登陆密码错误')
		if user_flag:
			return True
		else:
			return False