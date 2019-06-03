# -*- coding:utf-8 -*-
'''
通用配置文件
'''

class email_conf():
    '邮件发送配置'
    fromname = '18516292278@163.com'    #发件人
    toname = '773779347@qq.com'         #收件人,多个用,隔开
    subject = 'DevOps接口测试报告'       #邮件主题
    server = 'smtp.163.com'             #邮件服务器
    user = '18516292278'                #用户名
    passwd = 'lpb201212'                #授权码（不是密码）
    attchname = 'devops_report.html'   # 邮件中html附件名称

class log_conf():
    'log相关配置'
    filename = 'devops.log'

class mysql_conf():
    '数据库配置'
    host = "172.16.100.23"
    port = "3306"
    user = "root"
    password = "admin"
    dbname1 = "zgcollection"
    dbname2 = "zgcollmanager"