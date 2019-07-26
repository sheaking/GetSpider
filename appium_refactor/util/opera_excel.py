#coding=utf-8
import xlrd
from xlutils.copy import copy
#xlwd
class OperaExcel:
	def __init__(self,file_path=None,i=None):
		if file_path == None:
			#必须是xls的格式
			self.file_path = 'E:/Teacher/Imooc/AppiumPython/config/case.xls'
		else:
			self.file_path = file_path	
		if i == None:
			i=0
		self.excel = self.get_excel()
		self.data = self.get_sheets(i)
			
	def get_excel(self):
		'''
		获取excel
		'''
		excel = xlrd.open_workbook(self.file_path)
		return excel

	def get_sheets(self,i):
		'''
		获取sheets的内容
		'''
		tables = self.excel.sheets()[i]
		return tables

	def get_lines(self):
		'''
		获取excel行数
		'''
		lines = self.data.nrows
		return lines

	def get_cell(self,row,cell):
		'''
		获取单元格内容
		'''
		data = self.data.cell(row,cell).value
		return data

	#实际结果
	def write_value(self,row,value):
		read_value = self.excel
		write_data = copy(read_value)
		write_save = write_data.get_sheet(0)
		write_save.write(row,8,value)
		write_data.save(self.file_path)


if __name__ == '__main__':
	opera = OperaExcel()
	print (opera.get_lines())
	print (opera.write_value(6,'pass'))



