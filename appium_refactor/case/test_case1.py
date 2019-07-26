#coding=utf-8
import sys
# sys.path.append("E:/Teacher/Imooc/AppiumPython")
sys.path.append("D:/PycharmProjects/GetSpider")
import unittest
import HTMLTestRunner
import threading
import multiprocessing
from appium_refactor.util.server import Server
import time
from appium import webdriver
from appium_refactor.business.login_business import LoginBusiness
from appium_refactor.util.write_user_command import WriteUserCommand

class ParameTestCase(unittest.TestCase):
	def __init__(self,methodName='runTest',parame=None):
		super(ParameTestCase,self).__init__(methodName)
		global parames
		parames = parame

class CaseTest(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		print "setUpclass---->",parames
		cls.login_business = LoginBusiness(parames)

	def setUp(self):

		print "this is setup\n"


	def test_01(self):
		print "test case 里面的参数",parames
		self.login_business.login_pass()


		#self.assertNotEqual(1,2)
		#self.assertTrue(flag)
		#self.assertFalse(flag)
	#@unittest.skip("CaseTest")
	def test_02(self):
		self.login_business.login_user_error()
		print "this is case02\n"
		self.assertTrue(True)
	def tearDown(self):
		time.sleep(1)
		print "this is teardown\n"
		if sys.exc_info()[0]:
			self.login_business.login_handle.login_page.driver.save_screenshot("../jpg/test02.png")

	@classmethod
	def tearDownClass(cls):
		time.sleep(1)
		print "this is class teardown\n"
		#cls.driver.quit()

def appium_init():
	server = Server()
	server.main()

def get_suite(i):
	print "get_suite里面的",i
	suite = unittest.TestSuite()
	suite.addTest(CaseTest("test_02",parame=i))
	suite.addTest(CaseTest("test_01",parame=i))
	
	#unittest.TextTestRunner().run(suite)
	html_file = "E:/Teacher/Imooc/AppiumPython/report/report"+str(i)+".html"
	fp = file(html_file,"wb")
	HTMLTestRunner.HTMLTestRunner(stream=fp).run(suite)
def get_count():
	write_user_file = WriteUserCommand()
	count = write_user_file.get_file_lines()
	return count

# 用多进程，那样不会出错
if __name__ == '__main__':
	appium_init()
	#get_suite(0)
	threads = []
	for i in range(get_count()):
		print i
		t = multiprocessing.Process(target=get_suite,args=(i,))
		threads.append(t)
	for j in threads:
		j.start()

		#time.sleep(1)
	#time.sleep(80)
