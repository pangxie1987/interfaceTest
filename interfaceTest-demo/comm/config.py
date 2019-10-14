# -*- coding:utf-8 -*-
'''
通用配置文件
'''
IsSmoke = 1     # 0-非冒烟 1-冒烟
apicount = []   # 接口数量，统计接口用

class project_conf():
    '项目通用配置'
    project = 'demo'    # 项目名称

class email_conf():
    '邮件发送配置'
    fromname = '18516292278@163.com'    #发件人
    toname = '18516292278@163.com'      #收件人,多个用,隔开
    subject = '【DEMO项目】接口测试报告'  #邮件主题
    server = 'smtp.163.com'             #邮件服务器
    user = '18516292278'                #用户名
    passwd = 'lpb201212'                #授权码（不是密码）
    
class mysql_conf():
    '测试用例数据库配置'
    host = "172.16.101.223"
    port = "3306"
    user = "root"
    password = "admin"

class result_db():
    '测试结果数据库配置'
    table = "result"
    dbname = 'testresult'
    isinsert = 1    # 0-测试结果不入库，1-测试结果入库