#-*- coding:utf-8 -*-
'''
登录接口
集合系统登录机制
1、请求登录页面，服务器返回一个session（此时的session是无登录状态的）；
2、调用登录接口，带上步骤1的session，
'''
import os
import re
import sys
import base64
import datetime
import time
fapath = os.path.dirname(os.path.dirname(__file__))
fapath = os.path.join(fapath, '../')
sys.path.append(fapath)
import json
import requests
import unittest
from bs4 import BeautifulSoup
from comm.readjson import read
from comm.logset import logger
from comm.mysql import mysqlconnect

path = os.path.dirname(os.path.dirname(__file__))
cookiefile = os.path.join(path, "datas\\"+"cookies.json")
url = read('commdata.json')['url']
header_www = read('headers.json')['header_www']
header_json = read('headers.json')['header_json']
user = read('userinfo.json')['userinfo']
successuser = read('userinfo.json')['successuser']
nophoneuser = read('userinfo.json')['nophoneuser']
frozenuser = read('userinfo.json')['frozenuser']
deleteuser = read('userinfo.json')['deleteuser']
cookie = read('cookies.json')

class Login(unittest.TestCase):
    '登录接口'
    globals()["sendsms"] = 0

    @classmethod
    def setUp(self):
        self.db = mysqlconnect('zgcollmanager')

    @classmethod
    def setUpClass(self):
        '获取登录页的cookie'
        r = requests.get(url=url+'/login')
        print(r.elapsed.total_seconds())    # 接口响应时间
        print(r.url)        # 必须有这一行，统计接口数量用
        Login.mycookie = r.cookies.get_dict()
        if '获取验证码' in r.text:
            globals()["sendsms"] = 1
            user['smsSend'] = "true"
            # 获取服务器时间（在登录页面中）
            Login.nowtime = re.findall('(?!\bsendSms\(\")\d{14}', r.text)
            Login.nowtime = Login.nowtime[0]
            logger.info('Login.nowtime=======%s'%(Login.nowtime))
        else:
            globals()["sendsms"] = 2
            user['smsSend'] = "false"
            # del user['phonecode']

    @classmethod
    def tearDownClass(self):
        self.db.closedb()

    def encode_base64(self):
        '构造发送的code，time+username形式(yyyymmddhhmmss+username),获取登录页面返回的服务器时间'
        # nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # code = (nowtime + user['username']).encode('utf-8')
        code = (Login.nowtime + user['username']).encode('utf-8')
        print('code=========',code)
        Login.data = base64.b64encode(code)
        logger.info(Login.data)
        return Login.data

    def encodedata(self):
        '构造发送的code，time+username形式(yyyymmddhhmmss+username)，使用本地时间'
        nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        code = (nowtime + user['username']).encode('utf-8')
        print('code=========',code)
        encodedata = base64.b64encode(code)
        logger.info(encodedata)
        return encodedata

    def test_a1_sendsms(self):
        '非法时间发送验证码请求'
        if globals()["sendsms"] ==1:
            print('*' * 30 + '需手机验证码时间，该用例忽略')
        else:
            payload = b'reqSmsCode='+self.encodedata()
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.text)
            self.assertEqual('发送正常', r.json()['message'])

    def test_b1_sendsms(self):
        '发送短信验证码-用户不存在'
        if globals()["sendsms"] ==1:
            user['username'] = 'admin0009'
            print('*'*30+'发送验证码')
            payload = b'reqSmsCode='+self.encode_base64()
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            #print(r.text)
            #Login.phonecode = r.json()['data']
            self.assertEqual('用户不存在或非正常状态!', r.json()['message'])
        else:
            print('*'*30+'不需要手机验证码')
            #Login.phonecode = ""

    def test_b2_sendsms(self):
        '发送短信验证码-非法参数'
        if globals()["sendsms"] ==1:
            payload = "JH222t0aW1lMX1hZG1pbg=="
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            self.assertIn('非法请求', r.json()['message'])
        else:
            print('*'*30+'不需要手机验证码')

    def test_b3_sendsms(self):
        '发送短信验证码-参数为空'
        if globals()["sendsms"] ==1:
            payload = ""
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            self.assertIn('非法请求', r.json()['message'])
        else:
            print('*'*30+'不需要手机验证码')

    def test_b4_sendsms(self):
        '发送短信验证码-用户名为空'
        if globals()["sendsms"] ==1:
            user ['username'] = ""
            print('*'*30+'发送验证码')
            payload = b'reqSmsCode='+self.encode_base64()
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            self.assertIn('登陆失败!用户名或密码错误', r.json()['message'])
        else:
            print('*'*30+'不需要手机验证码')

    def test_b5_sendsms(self):
        '发送短信验证码-无手机号'
        if globals()["sendsms"] ==1:
            #sql = 'select account from user where `status`=1 and phone='''
            #name = self.db.execute(sql)[0]
            #user['username'] = name
            sqlupdate = "update `user` set `phone`=''  where  account='%s'"%(nophoneuser['username'])
            self.db.update_data(sqlupdate)
            user['username'] = nophoneuser['username']
            print('*'*30+'发送验证码')
            payload = b'reqSmsCode='+self.encode_base64()
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            #print(r.text)
            #Login.phonecode = r.json()['data']
            self.assertEqual('手机号为空,请修改个人信息', r.json()['message'])
        else:
            print('*'*30+'不需要手机验证码')
            #Login.phonecode = ""

    def test_b6_sendsms(self):
        '发送短信验证码-冻结用户'
        if globals()["sendsms"] ==1:
            # sql = 'select account from user where `status`=2 and phone='''
            # name = self.db.execute(sql)[0]
            # user['username'] = name
            sqlupdate = "update `user` set `status`=2   where  account='%s'"%(frozenuser['username'])
            self.db.update_data(sqlupdate)
            user['username'] = frozenuser['username']
            print('*'*30+'发送验证码')
            payload = b'reqSmsCode='+self.encode_base64()
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            #print(r.text)
            Login.djphonecode = r.json()['data']
            self.assertEqual('用户不存在或非正常状态!', r.json()['message'])
        else:
            print('*'*30+'不需要手机验证码')
            #Login.phonecode = ""

    def test_b7_sendsms(self):
        '发送短信验证码-已删除的用户'
        if globals()["sendsms"] ==1:
            # sql = 'select account from user where `status`=3'
            # name = self.db.execute(sql)[0]
            # user['username'] = name
            sqlupdate = "update `user` set `status`=3   where  account='%s'"%(deleteuser['username'])
            self.db.update_data(sqlupdate)
            user['username'] = deleteuser['username']
            print('*'*30+'发送验证码')
            payload = b'reqSmsCode='+self.encode_base64()
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            #print(r.text)
            #Login.phonecode = r.json()['data']
            self.assertEqual('用户不存在或非正常状态!', r.json()['message'])
        else:
            print('*'*30+'不需要手机验证码')
            #Login.phonecode = ""

    #@unittest.skipUnless(globals()["sendsms"] ==1, '获取不到字符-请输入验证码，则不发送短信')
    def test_b8_sendsms(self):
        '发送短信验证码'
        if globals()["sendsms"] ==1:
            time.sleep(60)
            #user['username'] = 'admin'
            user['username'] = successuser['username']
            print('*'*30+'发送验证码')
            payload = b'reqSmsCode='+self.encode_base64()
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            #print(r.text)
            Login.phonecode = r.json()['data']
            self.assertEqual('发送正常', r.json()['message'])
        else:
            #user['smsSend'] = False
            print('*'*30+'不需要手机验证码')
            Login.phonecode = ""

    #@unittest.skipUnless(globals()["sendsms"] ==1, '获取不到字符-请输入验证码，则不发送短信')
    def test_b9_sendsms(self):
        '发送短信验证码-不能重复发送'
        if globals()["sendsms"] ==1:
            user['username'] = successuser['username']
            print('*'*30+'发送验证码')
            payload = b'reqSmsCode='+self.encode_base64()
            r =requests.post(url=url+'sendSMS', data=payload, headers=header_www)
            print(r.url)
            #print(r.text)
            #Login.phonecode = r.json()['data']
            self.assertEqual('不能重复发送', r.json()['message'])
        else:
            print('*'*30+'不需要手机验证码')
            #Login.phonecode = ""

    def test_c1_login(self):
        '登录请求-用户名为空'
        # if globals()["sendsms"] ==1:
        #     #user['phonecode'] = Login.phonecode
        #     user['username'] = ''
        #     print(user)
        #     r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        #     print(r.text)
        #     #self.assertIn('验证码不正确', r.text)
        #     self.assertIn('用户名或密码不存在', r.text)
        # else:
        user['username'] = ''
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('用户名或密码不存在', r.text)

    def test_c2_login(self):
        '登录请求-缺少参数username'
        # if globals()["sendsms"] ==1:
        #     #user['phonecode'] = Login.phonecode
        #     del user['username']
        #     print(user)
        #     r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        #     print(r.text)
        #     #self.assertIn('验证码不正确', r.text)
        #     self.assertIn('用户名或密码不存在', r.text)
        # else:
        del user['username']
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('用户名或密码不存在', r.text)

    def test_c3_login(self):
        '登录请求-用户名错误'
        # if globals()["sendsms"] ==1:
        #     #user['phonecode'] = Login.phonecode
        #     user['username'] = 'admin0009'
        #     print(user)
        #     r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        #     print(r.text)
        #     #self.assertIn('验证码不正确', r.text)
        #     self.assertIn('登陆失败!用户名或密码错误', r.text)
        # else:
        user['username'] = 'admin0009'
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('登陆失败!用户名或密码错误', r.text)

    def test_d1_login(self):
        '登录请求-密码为空'
        #user['phonecode'] = Login.phonecode
        user['username'] = successuser['username']
        user['password'] = ''
        #user['kaptcha'] = '888888'
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('用户名或密码不存在', r.text)

    def test_d2_login(self):
        '登录请求-缺少参数password'
        #user['phonecode'] = Login.phonecode
        user['username'] = successuser['username']
        del user['password']
        #user['kaptcha'] = '888888'
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('用户名或密码不存在', r.text)

    def test_d3_login(self):
        '登录请求-密码错误'
        #user['phonecode'] = Login.phonecode
        user['username'] = successuser['username']
        user['password'] = '123'
        #user['kaptcha'] = '888888'
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('登陆失败!用户名或密码错误！', r.text)

    def test_e1_login(self):
        '登录请求-未获取验证码'
        if globals()["sendsms"] ==1:
            #user['phonecode'] = Login.phonecode
            user['username'] = nophoneuser['username']
            user['password'] = nophoneuser['password']
            user['phonecode'] = ''
            print(user)
            r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
            print(r.url)
            print(r.text)
            self.assertIn('验证码不正确', r.text)
        else:
            print('*'*30+'不需要手机验证码,此用例忽略')

    def test_e2_login(self):
        '登录请求-验证码为空'
        #user['phonecode'] = Login.phonecode
        user['username'] = successuser['username']
        user['password'] = successuser['password']
        user['kaptcha'] = ''
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('验证码不正确', r.text)

    def test_e3_login(self):
        '登录请求-验证码错误'
        #user['phonecode'] = Login.phonecode
        user['username'] = successuser['username']
        user['password'] = successuser['password']
        user['kaptcha'] = '123'
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('验证码不正确', r.text)

    def test_e4_login(self):
        '登录请求-缺少参数kaptcha'
        #user['phonecode'] = Login.phonecode
        user['username'] = successuser['username']
        user['password'] = successuser['password']
        del user['kaptcha']
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('验证码不正确', r.text)

    def test_e5_login(self):
        '登录请求-验证码错误非数字'
        #user['phonecode'] = Login.phonecode
        user['username'] = successuser['username']
        user['password'] = successuser['password']
        user['kaptcha'] = 'aaaaaa'
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('验证码不正确', r.text)

    def test_f1_login(self):
        '登录请求-手机号为空'
        if globals()["sendsms"] ==1:
            user['username'] = successuser['username']
            user['password'] = successuser['password']
            user['kaptcha'] = successuser['kaptcha']
            user['phonecode'] = ''
            print(user)
            r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
            print(r.url)
            print(r.text)
            self.assertIn('验证码不正确', r.text)
        else:
            print('*'*30+'不需要手机验证码,此用例忽略')

    def test_f2_login(self):
        '登录请求-错误的手机号'
        if globals()["sendsms"] ==1:
            user['username'] = successuser['username']
            user['password'] = successuser['password']
            user['kaptcha'] = successuser['kaptcha']
            user['phonecode'] = '12345678901'
            print(user)
            r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
            print(r.url)
            print(r.text)
            self.assertIn('验证码不正确', r.text)
        else:
            print('*'*30+'不需要手机验证码,此用例忽略')

    def test_f3_login(self):
        '登录请求-缺少参数phonecode'
        if globals()["sendsms"] ==1:
            user['username'] = successuser['username']
            user['password'] = successuser['password']
            user['kaptcha'] = successuser['kaptcha']
            del user['phonecode']
            print(user)
            r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
            print(r.url)
            print(r.text)
            self.assertIn('验证码不正确', r.text)
        else:
            print('*'*30+'不需要手机验证码,此用例忽略')

    def test_g1_login(self):
        '登录请求-冻结用户'
        sqlupdate = "update `user` set `status`=2   where  account='%s'" % (frozenuser [ 'username' ])
        self.db.update_data ( sqlupdate )
        user [ 'username' ] = frozenuser [ 'username' ]
        user [ 'password' ] = frozenuser [ 'password' ]
        user [ 'kaptcha' ] = frozenuser [ 'kaptcha' ]
        if globals()["sendsms"] ==1:
            #sql = 'select account from user where `status`=2 and phone="" '
            #name = self.db.execute(sql)[0]
            user['phonecode'] = Login.djphonecode
            print(user)
            r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
            print(r.url)
            print(r.text)
            self.assertIn('验证码不正确', r.text)
        else:
            print(user)
            r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
            print(r.url)
            print(r.text)
            self.assertIn('登陆失败!用户名或密码错误', r.text)

    def test_g2_login(self):
        '登录请求-删除的用户'
        if globals()["sendsms"] ==2:
            #sql = 'select account from user where `status`=3'
            #name = self.db.execute(sql)[0]
            sqlupdate = "update `user` set `status`=3   where  account='%s'"%(deleteuser['username'])
            self.db.update_data(sqlupdate)
            user['username'] = deleteuser['username']
            user['password'] = deleteuser['password']
            user['kaptcha'] = deleteuser['kaptcha']
            print(user)
            r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
            print(r.url)
            print(r.text)
            self.assertIn('登陆失败!用户名或密码错误', r.text)
        else:
            print('*'*30+'不需要手机验证码,此用例忽略')

    def test_h1_login(self):
        '登录请求-登录成功'
        user['username'] = successuser['username']
        user['password'] = successuser['password']
        user['kaptcha'] = successuser['kaptcha']
        if globals()["sendsms"] ==1:
            user['phonecode'] = Login.phonecode
        print(user)
        r = requests.post(url=url+'login',data=user, headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        # 将cookie写入文件中
        with open(cookiefile, 'w') as f:
            json.dump(Login.mycookie,f )
        logger.info(Login.mycookie)
        self.assertIn('个人资料', r.text)


    def test_i1_logout(self):
        '登出操作'
        r = requests.get(url=url+'loginout', headers=header_www, cookies=Login.mycookie)
        print(r.url)
        print(r.text)
        self.assertIn('请输入用户名', r.text)

    # 退出后，再次登录
        r = requests.get(url = url + '/login')
        print(r.url)
        Login.mycookie = r.cookies.get_dict()
        self.test_h1_login()

if __name__ == '__main__':
    # suit = unittest.TestSuite()
    # suit.addTest(Login('test_d2_login'))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    unittest.main()