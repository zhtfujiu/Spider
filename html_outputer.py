# coding=UTF-8
# 输出口
import pymysql
from doing_mysql import Doing_mysql
class HtmlOutputer(object):

    def __init__(self):
        self.datas = []

    def collect_data(self, new_data):
        if new_data is None:
            return
        self.datas.append(new_data)


    def output_mysql(self): # 数据刷新到数据库
        doing_mysql = Doing_mysql()
        # 创建该词条的表
        data = self.datas[0]
        # data = data['title'].encode('utf-8')
        data = data['title']
        doing_mysql.do_create_entry_table(data)

        for data2 in self.datas:
            # doing_mysql.do_add_entrydata(data, data2['title'].encode('utf-8'), data2['url'], data2['summary'].encode('utf-8').replace("\n", ""))
            doing_mysql.do_add_entrydata(data, data2['title'], data2['url'],
                                     data2['summary'].replace("\n", ""))

        # 关闭SQL
        doing_mysql.do_end_sql()
