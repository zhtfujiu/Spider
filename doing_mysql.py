# coding=UTF-8
# 执行数据库的相关操作

import pymysql, xlsxwriter

class Doing_mysql(object):

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root_psw', db='baike', charset='utf8')
        self.cur = self.conn.cursor()
        # self.cur.execute('USE baike')  # 后面修改成自动创建数据表
        print '数据库已连接'


    # 执行查询SQL
    def do_select_mysql(self, sql):
        return self.cur.execute(sql)

    # 查询是否存在某某表
    def do_check_is_in(self, tablename):
        # sql_check = 'SELECT TABLE_NAME FROM information_schema.`TABLES` WHERE TABLE_SCHEMA=\'baike\' AND TABLE_NAME="' + unicode(
        #     tablename, 'utf-8') + '";'
        sql_check = 'SELECT TABLE_NAME FROM information_schema.`TABLES` WHERE TABLE_SCHEMA=\'baike\' AND TABLE_NAME="' + tablename.encode("utf-8") + '";'
        # 返回TRUE则证明不存在，FALSE则存在该表
        # print self.cur.execute(sql_check) == 0
        return self.cur.execute(sql_check) == 0

    # 创建个人表
    def do_create_info_table(self, username):
        # 首先检测数据库中是否存在该username的table
        if self.do_check_is_in(username):
            # 不存在该表，新建表格
            sql = 'CREATE TABLE ' + username.encode("utf-8") + ' (百度账号 CHAR(20) PRIMARY KEY,头像图片链接 CHAR(200), 百科等级 CHAR(3), 通过版本 CHAR(3), 优质版本 CHAR(3), 特色词条 CHAR(3), 提交版本 CHAR(3), 通过率 CHAR(3), 创建版本 CHAR(3), 财富值 CHAR(3));'
            self.cur.execute(sql)
            self.conn.commit()

        else:
            # 证明存在该表
            return


    # 创建爬取列表，以词条命名
    def do_create_entry_table(self, entry):
        if self.do_check_is_in(entry):
            # 证明不存在该表
            sql = 'CREATE TABLE ' + entry + ' (name CHAR(100) PRIMARY KEY,url TEXT, abscract TEXT);'
            self.cur.execute(sql)
            self.conn.commit()
            print '已为您与baike数据库中创建', entry, '数据表。'
        else:
            # 存在该表，不用新建表格
            print '您的baike数据库中已有', entry, '数据表。'
            return

    # 更新个人信息至百度百科个人账号表
    def do_add_userinfo(self, username, user_pic_url, user_level, tongguo, youzhi, tese, tijiao, tongguolv, chuangjian, caifuzhi):
        sql = 'insert into '+ username.encode("utf-8") +' (百度账号, 头像图片链接, 百科等级, 通过版本, 优质版本, 特色词条, 提交版本, 通过率, 创建版本, 财富值) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ' \
              '百度账号=百度账号, 头像图片链接=头像图片链接, 百科等级=百科等级, 通过版本=通过版本 , ' \
              '优质版本=优质版本 , 特色词条=特色词条 , 提交版本=提交版本 , 通过率=通过率 , 创建版本=创建版本 , 财富值=财富值'
        self.cur.execute(sql,(username.encode("utf-8"), user_pic_url, user_level, tongguo, youzhi, tese, tijiao, tongguolv, chuangjian, caifuzhi))
        self.conn.commit()

    # 更新爬取信息至该词条table
    def do_add_entrydata(self, entry, name, url, abscract):
        sql = 'insert into '+entry.encode("utf-8")+' (name, url, abscract) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=name, url=url, abscract=abscract;'
        self.cur.execute(sql, (name.encode("utf-8"), url, abscract.encode('utf-8')))
        self.conn.commit()

    # 导出至Excel
    def do_ecport2excel(self, tablename):
        try:
            self.cur.execute('select * from ' + tablename.encode("utf-8"))
            # 重置游标位置
            self.cur.scroll(0, mode='absolute')
            results = self.cur.fetchall()

            # 获取MYSQL里面的数据字段名称
            fields = self.cur.description
            workbook = xlsxwriter.Workbook('/Users/fujiu/Desktop/' + tablename.encode("utf-8") + '.xlsx')
            sheet = workbook.add_worksheet()

            # 写上字段信息
            for field in range(0, len(fields)):
                sheet.write(0, field, fields[field][0])

            # 获取并写入数据段信息
            for row in range(1, len(results) + 1):
                for col in range(0, len(fields)):
                    sheet.write(row, col, u'%s' % results[row - 1][col])

            workbook.close()
            print '导出Excel文件成功，请前往电脑桌面查看'
            return True
        except Exception, e:
            print '导出Excel文件失败', e
            return False

    # 获取预览信息（Data界面第一个功能需要）
    def do_getdata2grid(self, tablename, grid):
        try:
            self.cur.execute('select * from ' + tablename.encode("utf-8"))
            # 重置游标位置
            self.cur.scroll(0, mode='absolute')
            results = self.cur.fetchall()

            # 获取MYSQL里面的数据字段名称
            fields = self.cur.description

            # 写上字段信息
            for field in range(0, len(fields)):
                grid.SetCellValue(0, field, fields[field][0])

            if len(results) > 100:
                grid.AppendRows(len(results)-100)
                grid.Update()

            # 获取并写入数据段信息
            for row in range(1, len(results) + 1):
                for col in range(0, len(fields)):
                    grid.SetCellValue(row, col, u'%s' % results[row - 1][col])

            return True
        except Exception, e:
            print '获取预览信息失败', e
            return False


    # 获取预览信息（Data界面第一个功能需要）
    def do_DIYsql2grid(self, sql, grid):
        try:
            self.cur.execute(sql)
            # 重置游标位置
            self.cur.scroll(0, mode='absolute')
            results = self.cur.fetchall()

            # 获取MYSQL里面的数据字段名称
            fields = self.cur.description

            # 写上字段信息
            for field in range(0, len(fields)):
                grid.SetCellValue(0, field, fields[field][0])

            if len(results) > 100:
                grid.AppendRows(len(results)-100)
                grid.Update()

            # 获取并写入数据段信息
            for row in range(1, len(results) + 1):
                for col in range(0, len(fields)):
                    grid.SetCellValue(row, col, u'%s' % results[row - 1][col])

            return True
        except Exception, e:
            print 'SQL语句执行失败', e
            return False

    # 关闭数据库连接
    def do_end_sql(self):
        self.cur.close()
        self.conn.close()