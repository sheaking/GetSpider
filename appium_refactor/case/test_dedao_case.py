#coding=utf-8
import sys
# sys.path.append("E:/Teacher/Imooc/AppiumPython")
sys.path.append("D:/PycharmProjects/GetSpider")
import unittest
# import HTMLTestRunner
import multiprocessing
import threading
from appium_refactor.util.server import Server
import time
from appium import webdriver
from appium_refactor.business.login_business import LoginBusiness
from appium_refactor.business.overview_business import OverviewBusiness
from appium_refactor.util.write_user_command import WriteUserCommand

class ParameTestCase(unittest.TestCase):
	def __init__(self,methodName='runTest',parame=None):
		print('第几个类： ', parame)
		super(ParameTestCase,self).__init__(methodName)
		global parames
		parames = parame

class CaseTest(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		print ("setUpclass---->", parames)
		# cls.login_business = LoginBusiness(parames)
		cls.overview_business = OverviewBusiness(parames)

	def setUp(self):
		print ("this is setup\n")


	def test_dedao(self):
		print("测试得到", parames)
		self.overview_business.go_purchase_page()
		self.overview_business.go_crawl_column_and_article()

	def tearDown(self):
		time.sleep(1)
		print ("this is teardown\n")
		if sys.exc_info()[0]:
			self.overview_business.overview_handle.overview_page.driver.save_screenshot("../jpg/test.png")

	@classmethod
	def tearDownClass(cls):
		time.sleep(1)
		print ("this is class teardown\n")
		#cls.driver.quit()

def appium_init():
	'''
	根据设备信息，启动appium服务
	并且把命令写到yaml文件中，供base_driver调用
	'''
	server = Server()
	server.main()

def get_suite(i):
	print("get_suite里面的",i)
	suite = unittest.TestSuite()
	suite.addTest(CaseTest("test_dedao",parame=i))
	# suite.addTest(CaseTest("test_01",parame=i))
	
	unittest.TextTestRunner().run(suite)
	# html_file = "E:/Teacher/Imooc/AppiumPython/report/report"+str(i)+".html"
	# fp = file(html_file,"wb")
	# HTMLTestRunner.HTMLTestRunner(stream=fp).run(suite)




def get_count():
	write_user_file = WriteUserCommand()
	count = write_user_file.get_file_lines()
	return count


# 用多进程，那样不会出错
if __name__ == '__main__':
	appium_init()
	processes = []
	for i in range(get_count()):
		print(i)
		t = multiprocessing.Process(target=get_suite,args=(i,))
		# t = threading.Thread(target=get_suite,args=(i,))
		processes.append(t)
	for j in processes:
		j.start()

	# # 进行阻塞
	# for k in processes:
	# 	k.join()
