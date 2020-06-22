#-*- coding:utf-8 -*-
'''
登陆及access_token处理
'''
import os
import re
import sys
import datetime
import time
fapath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(fapath)
import json
import requests
import unittest
from comm.readjson import read
from comm.logset import logger
from comm.mysql import mysqlconnect

path = os.path.dirname(os.path.dirname(__file__))
tokenfile = os.path.join(path, "datas", "access_token.json")
url = read('commdata.json')['gateway']
header_www = read('headers.json')['header_www']
header_json = read('headers.json')['header_json']
userinfo = read('userinfo_zt.json')['userinfo_']

class Login(unittest.TestCase):
    '登陆-获取access_token'

    @classmethod
    def setUpClass(cls):
        print('1')

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def test_a_gettoken(self):
        '获取access_token-无用户信息'
        datas={
            "Authorization": "1222",
            "client_id": "webApp",
            "client_secret": "webApp"
            }
        mytoken = {"access_token":""}
        r = requests.post(url=url+'api-auth/oauth/client/token',  headers=datas)
        logger.info(r.text)
        print(r.url)
    #     # mytoken['access_token'] = 'Bearer ' + r.json()['access_token']
    #     # print('access_token:%s'%mytoken)
    #     # # 将access_token写入文件中
    #     # with open(tokenfile, 'w') as f:
    #     #     json.dump(mytoken,f )
    #     # logger.info(mytoken)
    @classmethod
    def test_a_getusertoken(self):
        '获取access_token-根据用户名密码获取'
        headers={
            "Authorization": "1222",
            "client_id": "webApp",
            "client_secret": "webApp"
            }
        # datas = {
        #     "username": "admin",
        #     "password": "admin"
        # }
        mytoken = {"access_token":""}
        r = requests.post(url=url+'api-auth/oauth/user/token',  data=userinfo, headers=headers)
        logger.info(r.text)
        print(r.url)
        mytoken['access_token'] = 'Bearer ' + r.json()['access_token']
        logger.info('access_token:%s'%mytoken)
        # 将access_token写入文件中
        with open(tokenfile, 'w') as f:
            json.dump(mytoken,f )
        logger.info(mytoken)
    
if __name__ == '__main__':
    unittest.main()