# -*- coding:utf-8 -*-

import unittest
import os
import sys
import time
import shutil
from comm import HTMLTestRunner
from comm.logset import logger
from comm.email import send_email
from comm.logset import get_host_ip, testnet


import xmlrunner
from BeautifulReport import BeautifulReport as bf
'''
使用该模块运行所以测试案例，并生成测试报告
'''

#获取案例所在目录
case_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cases'))

#报告目录，不存在则创建
report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'report'))
if not os.path.exists(report_path):
    os.mkdir(report_path)

#历史报告目录，不存在则创建
his_report_path = os.path.join(os.path.dirname(__file__), "his_report")
if not os.path.exists(his_report_path):
    os.mkdir(his_report_path)

def mvreport(npaht,hispath):
    '''
    将报告移动到历史目录
    npath       当前报告文件目录
    hispath     历史报告文件目录
    '''    
    allfiles = []
    for root, dirs, files in os.walk(npaht):
        for file in files:
            if os.path.splitext(file)[1] == '.html' or os.path.splitext(file)[1] == '.xml':  
                allfiles.append(file)  
    print(allfiles)
    for mvfile in allfiles:
        shutil.move(os.path.join(npaht,mvfile), hispath)

def all_case():
    '获取所以要执行的案例,pattern规则'
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test_*.py",top_level_dir=None)
    print (discover)
    return discover

    # 单个suit进行添加
    # suite = unittest.TestSuite()
    # suite.addTest(test_collection_tb1.Tb1)
    # return suite

def report_xml(reppath):
    '生成xml格式报告,reppath为报告目录'
    suite=unittest.TestSuite()
    [suite.addTest(case) for case in all_case()]
    # with open(os.path.join(report_path, 'mytest_xml.xml'),'wb+') as f:
    runner_a = xmlrunner.XMLTestRunner(output=report_path)  #指定生成目录
    runner_a.run(suite)   #运行用例

def report_html(reppath):
    '使用HTMLTestRunner生成html格式的测试报告'
    fp = open(reppath, 'wb+')
    runner_b = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"DevOps接口测试报告", description=u"用例执行情况")
    runner_b.run(all_case())
    fp.close()

def run_toga():
    report_html(os.path.join(report_path, report_name+".html"))
    report_xml(report_path)

def report_bf(reppath, fname):
    '使用BeautifulReport库生成格式更美观的html报告'
    run = bf(all_case()) #实例化BeautifulReport模块
    run.report(filename=fname, report_dir=reppath, description='DevOps接口测试报告')

if __name__ == '__main__':
    logger.info('本次执行地址：%s'%(get_host_ip()))
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    mvreport(report_path, his_report_path)
    # 创建新的报告文件
    # report_abspsth = os.path.join(report_path,"result_"+now+".html")
    report_name = "report_"+now
    logger.info('report_name:%s'%report_name)

    # 执行所有的case
    try:
        if testnet() == 0:
            logger.info('网络正常，开始执行测试任务')
            report_html(os.path.join(report_path, report_name+".html"))
            # report_xml(report_path)
            # report_bf(report_path, report_name)
            flag = '测试任务执行成功'
        else:
            logger.info('测试环境网络异常，请检查！！！')
            flag = '测试环境网络异常，请检查！！！'
    except:
        flag = '测试任务执行出现异常，请检查！！！'
    finally:
        send_email(os.path.join(report_path, report_name+".html"), flag)
