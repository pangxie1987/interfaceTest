# -*- coding:utf-8 -*-
'''
通用配置文件
'''
IsSmoke = 1     # 执行方式：0-非冒烟测试 1-冒烟测试
apicount = []   # 统计接口数量用，无需配置
dblastid = 0    # 数据库入库的id

class project_conf():
    '项目通用配置'
    project = 'demo'    # 项目名称

class email_conf():
    '邮件发送配置'
    fromname = '18516292278@163.com'    # 发件人名称
    sender = '18516292278@163.com'      # 发件人邮箱
    toname = '测试组成员'                #收件人名称
    # receivers = ['18516292278@163.com'] #收件人邮箱
    receivers = '18516292278@163.com'   #收件人邮箱
    subject = '【DEMO项目】接口测试报告'  #邮件主题
    server = 'smtp.163.com'             #邮件服务器
    user = '18516292278'                #用户名
    passwd = 'lpb201212'                #授权码（不是密码）
    attchname = 'demo_report.html'     # 邮件中html附件名称
    
class mysql_conf():
    '测试用例数据库配置'
    host = "172.16.101.223"
    port = "3306"
    user = "root"
    password = "admin"

class result_db():
    '测试结果数据库配置'
    host = "172.16.101.223"
    port = "3306"
    user = "root"
    password = "admin"
    project = 'ztbiz'       # 项目名称
    table = "result"    # 测试结果统计
    apitable = 'apicount'   #各项目接口数量统计
    dbname = 'testresult'
    isinsert = 1    # 0-测试结果不入库，1-测试结果入库
	
class oracle_conf():
    'oracle数据库配置'
    host = "172.16.100.155"
    port = "1521"
    user = "hsfk"
    password = "hsfk"
    dbname = "TBDATA"
    dbname2 = "zgcollmanager"

class result_devops():
    'Devops测试结果库'
    host = "172.16.101.223"
    port = "3306"
    user = "root"
    password = "admin"
    project = 'ztbiz'       # 项目名称
    table = "DEVOPS_AUTO_TESTCASE_HIS_STATISTICS"    # 测试结果统计
    dbname = 'tebonxdevops'
    isinsert = 1                        # 0-测试结果不入库，1-测试结果入库
    creater = 'AutoAPI'                 # 测试结果创建人-REC_CREATER&REC_MODIFIER
    TASK_ID = 1001                       # 任务ID-由jenkins传入
    BUILD_NUMBER = 2002                  # 构建号-由jenkins传入
    projectKey = "JG"                   # Devops中的项目编号（projectCode）
    username = 'admin'
    mypasswd = 'admin'
    gateway = 'http://172.16.101.224:9200'
    client_id = 'webApp'
    client_secret = 'webApp'
    isinsertcase = 1                    # 0-测试用例不入库，1-测试用例入库