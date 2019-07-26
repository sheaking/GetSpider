#coding=utf-8
from appium_refactor.util.dos_cmd import DosCmd
from appium_refactor.util.port import Port
import threading
import time
from appium_refactor.util.write_user_command import WriteUserCommand
'''
主要用来获取真正的设备信息
对dos_cmd和port进行进一步封装
然后启动服务，关闭服务
启动服务器和关闭服务还需要通过yaml文件把启动命令传到appium中
'''
class Server:
	def __init__(self):
		self.dos = DosCmd()
		# 从命令行中获取设备列表
		self.device_list = self.get_devices()
		self.write_file = WriteUserCommand()
	def get_devices(self):
		'''
		获取设备信息
		'''
		devices_list = []
		result_list = self.dos.excute_cmd_result('adb devices')
		if len(result_list)>=2:
			for i in result_list:
				if 'List' in i:
					continue
				devices_info = i.split('\t')
				if devices_info[1] == 'device':
					devices_list.append(devices_info[0])
			return devices_list
		else:
			return None
	def create_port_list(self,start_port):
		'''
		创建可用端口
		'''
		port = Port()
		port_list = []
		port_list = port.create_port_list(start_port,self.device_list)
		return port_list

	def create_command_list(self,i):
		'''
		生成命令
		'''
		#appium -p 4700 -bp 4701 -U 127.0.0.1:21503
		
		command_list = []
		appium_port_list = self.create_port_list(4700)
		bootstrap_port_list = self.create_port_list(4900)
		device_list = self.device_list
		command = "appium -p " + str(appium_port_list[i]) + " -bp " + str(bootstrap_port_list[i]) + " -U "+ device_list[i] + " --no-reset --session-override --log ../log/test2.log"
		# command = "appium -p " + str(appium_port_list[i]) + " -bp " + str(bootstrap_port_list[i]) + " -U "+ device_list[i] + " --no-reset --log ../log/test2.log"
		#appium -p 4723 -bp 4726 -U 127.0.0.1:62001 --no-reset --session-override --log E:/Teacher/Imooc/AppiumPython/log/test01.log
		command_list.append(command)
		self.write_file.write_data(i,device_list[i],str(bootstrap_port_list[i]),str(appium_port_list[i]))

		return command_list

	def start_server(self,i):
		'''
		执行命令，启动服务
		'''
		# 这里不能循环遍历command_list，因为那样os是同一个线程下的，即同一个cmd窗口下的，会只启动一个而已
		self.start_list = self.create_command_list(i)
		print (self.start_list)

		self.dos.excute_cmd(self.start_list[0])

	def kill_server(self):
		server_list = self.dos.excute_cmd_result('tasklist | find "node.exe"')
		if len(server_list)>0:
			self.dos.excute_cmd('taskkill -F -PID node.exe')

	def main(self):
		thread_list = []
		self.kill_server()
		self.write_file.clear_data()
		# 根据设备个数来决定启动多少个线程
		for i in range(len(self.device_list)):
			appium_start = threading.Thread(target=self.start_server,args=(i,))
			thread_list.append(appium_start)
		for j in thread_list:
			j.start()
		# 必须sleep，不然出错，因为yaml文件这个时候无内容
		time.sleep(20)


if __name__ == '__main__':
	server = Server()
	print (server.main())
