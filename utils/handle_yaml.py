
import yaml
import sys
# sys.path.append("E:/Teacher/Imooc/AppiumPython")
# sys.path.append("D:/PycharmProjects/GetSpider")


class WriteUserCommand():
	def read_data(self):
		'''
		加载yaml数据
		'''
		with open("D:/PycharmProjects/GetSpider/temp_file/count.yaml") as fr:
			data = yaml.load(fr)
		return data

	def get_value(self,key):
		'''
		获取value
		'''
		data = self.read_data()
		value = data[key]
		return value

	def write_data(self,num):
		'''
		写入数据
		'''
		data = self.join_data(num)
		with open("D:/PycharmProjects/GetSpider/temp_file/count.yaml", "w") as fr:
			yaml.dump(data,fr)

	def join_data(self,num):
		data = {
			"num": num
		}
		return data

	def clear_data(self):
		with open("../temp_file/count.yaml","w") as fr:
			fr.truncate()
		fr.close()

	def get_file_lines(self):
		data = self.read_data()
		return len(data)


if __name__ == '__main__':
	w = WriteUserCommand()
	# w.write_data(13)
	print(type(w.get_value('num')))