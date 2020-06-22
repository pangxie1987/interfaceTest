# -*- coding:utf-8 -*-

import logging
import os
import time
import socket
import sys
fapath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(fapath)
import requests
from comm.readjson import read
from comm.config import project_conf

url = read('commdata.json')['gateway']
logpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "report")
print(logpath)

def loginit():
    '''
    #定义日志格式，并将日志同时向屏幕输出并写入文件
    '''
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    #datefmt='%a, %d %b %Y %H:%M:%S',
                    datefmt= '%Y-%m-%d %H:%M:%S',
                    filename=os.path.join(logpath, project_conf.project+'.log'),
                    filemode='w')
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

loginit()
logger=logging.getLogger(__name__)

def get_host_ip():
    '查询IP地址'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def testnet():
    '判断当前网络情况'
    newurl = url.replace('http://', '')
    newurl = newurl.split(':')[0]
    ip = newurl.replace('/', '')
    # 如果网络通则netnow==0
    cmd = 'ping '+ip
    i = 0
    for i in range(3):
        net = os.system(cmd)
        if net == 0:
            logger.info('当前%s正常'%ip)
            break
        else:
            logger.info('网络异常,第%s次尝试'%(i+1))
            time.sleep(120) #等待120S后重试           
    return net

if __name__ == '__main__':
    print(testnet())