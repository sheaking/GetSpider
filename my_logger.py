#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a logger module '

__author__ = 'Shea Jin'

import logging
import logging.handlers
import os
import sys
sys.path.append('../')  # 新加入的


#用字典保存日志级别
format_dict = {
   1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}
# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger():
    def __init__(self, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)

        # 创建一个handler，用于写入日志文件
        # fh = logging.FileHandler(logname)
        # fh.setLevel(logging.DEBUG)

        #把日志写入这个文件，如果文件夹不存在就创建
        if not os.path.exists('../log'):
            os.mkdir('../log')

        #存储最近7天的错误跟踪日志,超过7天就删除
        time_handler = logging.handlers.TimedRotatingFileHandler('../log/error_log', when='D', interval=1, backupCount=7)
        time_handler.suffix = '%Y-%m-%d.log'
        #只要是日志级别大于WARNING，就会写入文件
        time_handler.setLevel(logging.WARNING)

        # 再创建一个handler，用于输出到控制台
        console_hanlder = logging.StreamHandler()
        console_hanlder.setLevel(logging.INFO)

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[5]
        time_handler.setFormatter(formatter)
        console_hanlder.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(time_handler)
        self.logger.addHandler(console_hanlder)

    def getlog(self):
        return self.logger

    # @classmethod
    # def test(self):
    #     print('hah')

if __name__ == '__main__':
    logger = Logger(logger="Shea").getlog()
    try:
        print('try')
        i = 10/0
    except BaseException as e:
        print('yic')
        logger.error('错误')

    print('token')

    # Logger.test()
