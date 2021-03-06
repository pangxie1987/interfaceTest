# -*- coding:utf-8 -*-
'''
mysql数据库操作
'''
import os
import sys
casepath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) 
sys.path.append(casepath)
import json
import pymysql
import os
from comm.config import mysql_conf, result_devops

host = mysql_conf.host
port = mysql_conf.port
user = mysql_conf.user
passwd = mysql_conf.password

class mysqlconnect(object):
    '封装数据库操作方法'
    def __init__(self, dbname):
        self.conn = pymysql.connect(host=host, db=dbname, user=user, passwd=passwd, use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        '执行并返回单条数据'
        self.cursor.execute(sql)
        sqldata = self.cursor.fetchone()
        # print(sqldata)
        # 返回的是一个元组
        return sqldata

    def execute_all(self, sql):
        '执行并返回全部数据'
        self.cursor.execute(sql)
        sqldata = self.cursor.fetchall()
        return sqldata

    def delete_data(self, sql):
        '删除数据'
        self.cursor.execute(sql)
        self.cursor.execute('commit')
        return 

    def update_data(self, sql):
        '修改数据'
        self.cursor.execute(sql)
        self.cursor.execute('commit')
        return

    def getlastid(self,sql):
        '插入数据并获取自增id'
        self.cursor.execute(sql)
        newid = self.cursor.lastrowid
        self.cursor.execute('commit')
        print('the last id=%s'%newid)
        return newid

    def closedb(self):
        '关闭数据库连接'
        self.conn.close()

class mysqlconnectcommon(object):
    '封装数据库操作方法-测试结果库'
    def __init__(self, host, port, user, passwd, dbname):
        self.conn = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=dbname, use_unicode=True, charset="utf8", connect_timeout=100)
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        '执行并返回单条数据'
        self.cursor.execute(sql)
        sqldata = self.cursor.fetchone()
        # print(sqldata)
        # 返回的是一个元组
        return sqldata

    def execute_all(self, sql):
        '执行并返回全部数据'
        self.cursor.execute(sql)
        sqldata = self.cursor.fetchall()
        return sqldata

    def delete_data(self, sql):
        '删除数据'
        self.cursor.execute(sql)
        self.cursor.execute('commit')
        return 

    def update_data(self, sql):
        '修改数据'
        self.cursor.execute(sql)
        self.cursor.execute('commit')
        return

    def getlastid(self,sql):
        '插入数据并获取自增id'
        try:

            self.cursor.execute(sql)
            newid = self.cursor.lastrowid
        except Exception as e:
            print(e)
            raise e
        self.cursor.execute('commit')
        print('the last id=%s'%newid)
        return newid

    def closedb(self):
        '关闭数据库连接'
        self.conn.close()

if __name__ == '__main__':
    sql = "select count(*) from collection_product_info"
    db = mysqlconnect('zgcollection')
    print(db.execute(sql)[0])
    # data = db.execute(sql)[0]
    # db.execute('commit')
    db.closedb()