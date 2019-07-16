# -*- coding: utf-8 -*-
from config.settings import *
from my_logger import Logger
import pymysql

#存储模块
class MySQL():
    def __init__(self):
        self.logger = Logger(LOGGER_NAME).getlog()

        self.host = MYSQL_HOST
        self.username = MYSQL_USER
        self.password = MYSQL_PASSWORD
        self.port = MYSQL_PORT
        self.database = MYSQL_DATABASE

    def get_connection(self):
        try:
            self.db = pymysql.connect(self.host, self.username, self.password, self.database, charset='utf8', port=self.port)
            self.cursor = self.db.cursor()
            print('获取数据库链接成功')
            return True
        # except pymysql.MySQLError as e:
        #     print(e.args)
        except:
            print('获取数据库链接失败')
            self.logger.error('获取数据库链接失败')
            return False


    def close_connection(self):

        try:
            if self.db:
                self.db.close()
                print('关闭数据库链接成功')
                return True
        except :
            self.logger.error('关闭数据库链接失败')
            print('关闭数据库链接失败')
            return False
        #如果用下面的，程序就挂了
        # except pymysql.MySQLError as e:
        #     print(e.args)

        # print(self.db)


    #插入的时候要判断这个url是否在数据库中
    def insert(self, table, data):
        """
        插入数据
        :param table:
        :param data:
        :return:
        """
        # self.select(table,data)

        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))

        sql_query = 'insert into %s (%s) values (%s)' % (table, keys, values)
        # print(self.select(table, 'count(url)', 'url = \"' + data.get('url') + '\"'))
        try:
             #判断要插入的数据是否在数据库中存在，按照不同表的唯一标识进行查询
            sql_filter = ''
            if table == 'tb_column':
                sql_filter = 'column_id = \"' + str(data.get('column_id')) + '\"'

            elif table == 'category':
                sql_filter = 'category_id = \"' + str(data.get('category_id')) + '\"'

            elif table == 'source':
                sql_filter = 'source_id = \"' + str(data.get('source_id')) + '\"'

            elif table == 'author':
                sql_filter = 'author_id = \"' + str(data.get('author_id')) + '\"'

            elif table == 'ext_attribute':
                sql_filter = 'article_id = \"' + str(data.get('article_id')) + '\"' + ' and ' + 'attribute_name=\"' + str(data.get('attribute_name')) + '\"'

            elif table == 'article':
                sql_filter = 'article_id = \"' + str(data.get('article_id')) + '\"'

            elif table == 'article_author':
                sql_filter = 'article_id = \"' + str(data.get('article_id')) + '\"'

            elif table == 'article_category':
                sql_filter = 'article_id = \"' + str(data.get('article_id')) + '\"'

            elif table == 'article_column':
                sql_filter = 'article_id = \"' + str(data.get('article_id')) + '\"'

            elif table == 'article_source':
                sql_filter = 'article_id = \"' + str(data.get('article_id')) + '\"'

            if sql_filter:
                if self.select(table,'count(1)', sql_filter) == ((0,),):
                    if self.cursor.execute(sql_query, tuple(data.values())):
                        # print(self.select(table,'count(url)', 'url = \"' + data.get('url') + '\"'))
                        print(table + '：数据插入成功')
                        self.db.commit()
                else:
                    print(table + '： 数据库中该数据已经存在，插入失败')

        except Exception as e:

            print(table + '： 插入方法出现异常，数据插入失败')
            print(e)
            self.logger.error('插入方法出现异常，数据插入失败')
            self.db.rollback()

    def select(self, table, columns, filter):

        #如果类型为list类型，就要拼接
        if type(columns) == type([1,2]):
        # if isinstance(columns,list):
            columns = ', '.join(columns)

        sql_query = 'select %s from %s where %s' % (columns, table, filter)
        print('查询语句为: %s' % sql_query)
        try:
            self.cursor.execute(sql_query)
            print('查询出的数量：',self.cursor.rowcount)
            results = self.cursor.fetchall()
            # print(results)
            return results
        except:
            print('查询方法出现异常')
            self.logger.error('查询方法出现异常')


    def update(self,table,setter,filter):
        sql_query = 'update %s set %s where %s' % (table,setter,filter)
        print(sql_query)
        try:
            self.cursor.execute(sql_query)
            print('success')
            self.db.commit()
        except:
            print('failed')
            self.logger.error('更新方法出现异常')
            self.db.rollback()


if __name__ == '__main__':
    mysql = MySQL()
    mysql.get_connection()
    # mysql.update(TARGET_TABLE,'published = 1','url = ' + '\"https://futurism.com/russia-new-shotgun-wielding-drone-action/\"')
    if mysql.close_connection():
        print('haha')
