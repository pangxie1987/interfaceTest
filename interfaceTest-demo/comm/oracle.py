# -*- coding:utf-8 -*-
'''
Oracle数据库操作
执行机需按照Oracle客户端，配置tnsnames.ora
'''
import os
import sys
casepath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) 
sys.path.append(casepath)
import json
import cx_Oracle as oracle
import os
from comm.config import oracle_conf

#db = oracle.connect('hsfk/hsfk@172.16.100.155:1521/TBDATA')
#cursor = db.cursor()
#cursor.execute('select sysdate from dual')
#data = cursor.fetchone()
#print('Database time:%s' % data)
#cursor.close()
#db.close()

host = oracle_conf.host
port = oracle_conf.port
dbname = oracle_conf.dbname
user = oracle_conf.user
passwd = oracle_conf.password

class oracleconnect(object):
    '封装数据库操作方法'
    def __init__(self, dbname):
        try:
            self.conn = oracle.connect(user+"/"+passwd+"@"+host+":"+port+"/"+dbname)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

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

    def closedb(self):
        '关闭游标，数据库连接'
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    sql = "select distinct vc_cpdm from tbdata.v_zg_gzb"
    db = oracleconnect('TBDATA')
    print(db.execute_all(sql))
    # data = db.execute(sql)[0]
    # db.execute('commit')
    db.closedb()