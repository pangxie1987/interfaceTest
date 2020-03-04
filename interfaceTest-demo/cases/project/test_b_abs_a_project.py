# -*- coding:utf-8 -*-
'''
项目管理接口
'''
import os
import sys
fapath = os.path.dirname(os.path.dirname(__file__))
fapath = os.path.join(fapath, '../')
sys.path.append(fapath)
import requests
import unittest
from comm.readjson import read
from comm.mysql import mysqlconnect
from comm.commdata import cdatas
from comm.logset import logger

url = read('commdata.json')['url']
project = read('project.json')['project']
nproject = read('project.json')['nproject']
header_www = read('headers.json')['header_www']
header_json = read('headers.json')['header_json']
#cookie = read('cookies.json')

class Project(unittest.TestCase):
    '项目管理'
    
    @classmethod
    def setUpClass(cls):
        cls.db = mysqlconnect('zgcollection')
        cls.cookie = read('cookies.json')

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def test_a0_gettee(self):
        '获取托管人数据'
        r = requests.post(url=url+'agencyinfo/getTrusteeList', headers=header_www, cookies=self.cookie)
        print(r.text)
        Project.teeid = r.json()[0]['id']
        self.assertEqual(200, r.status_code)

    def test_a1_addproject(self):
        '新增项目-标准'
        project['trustee'] = Project.teeid
        r = requests.post(url=url+'project_list/addProject', data=project, headers=header_www, cookies=self.cookie)
        logger.info(self.cookie)
        logger.info(r.text)
        # 如果名称已存在，删除后新增
        if r.json()['message'] == '项目名称已存在!':
            sql = "delete from collection_project_approval where name='%s'"%(project['name'])
            self.db.delete_data(sql)
            print('delete same name productinfo')
            r = requests.post(url=url+'project_list/addProject', params=project, headers=header_json, cookies=self.cookie)
        self.assertEqual("添加成功!", r.json()['message'])

    def test_b0_listproject(self):
        '获取项目id-标准'
        r = requests.post(url=url+'project_list/queryProject', data={'page':1,'limit':100,'status':'','name':project['name']}, headers=header_json, cookies=self.cookie)
        print(r.text) 
        projectsid = []
        for projects in r.json()['data']:
            projectsid.append(projects['id'])
        projectsid.sort(reverse = True)
        cdatas.projectid = projectsid[0]
        logger.info('标准项目id=%s'%(projectsid[0]))
        self.assertEqual(200, r.status_code)

    def test_b1_prostatus(self):
        '校验项目状态-新增为1'
        r = requests.post(url + '/project_list/queryProjectById', params={'id': cdatas.projectid}, headers=header_www, cookies=self.cookie)
        status = r.json()['data'][0]['status']
        self.assertEqual(1, status)

    def test_c_addproject(self):
        '新增项目-非标准'
        nproject['trustee'] = Project.teeid
        r = requests.post(url=url+'projectinfo/addProject', params=nproject, headers=header_json, cookies=self.cookie)
        logger.info(self.cookie)
        logger.info(r.text)
        # 如果名称已存在，删除后新增
        if r.json()['message'] == '项目名称已存在':
            sql = "delete from collection_project_approval where name='%s'"%(nproject['name'])
            self.db.delete_data(sql)
            print('delete same name productinfo')
            r = requests.post(url=url+'projectinfo/addProject', params=nproject, headers=header_json, cookies=self.cookie)
        self.assertEqual("新增成功", r.json()['message'])
        
    def test_d_listproject(self):
        '获取项目id-非标'
        r = requests.post(url=url+'projectinfo/list', data={'page':1,'limit':100,'status':'','name':nproject['name']}, headers=header_json, cookies=self.cookie)
        print(r.text)
        nprojectsid = []
        for nprojects in r.json()['data']:
            nprojectsid.append(nprojects['id'])
        nprojectsid.sort(reverse = True)
        cdatas.nprojectid = nprojectsid[0]
        logger.info('非标项目id=%s'%nprojectsid[0])
        self.assertEqual(200, r.status_code)

    def test_e_prostatus(self):
        '校验项目状态-新增为1'
        r = requests.post(url + 'projectinfo/viewProject', params={'id': cdatas.nprojectid}, headers=header_www, cookies=self.cookie)
        status = r.json()['data']['status']
        self.assertEqual(1, status)

    def test_f0_addproject(self):
        '新增项目-定向'
        nproject['name'] = '接口测试专用项目-定向'
        nproject['productType'] = 3
        r = requests.post(url=url+'orientation/projectinfo/addProject', params=nproject, headers=header_json, cookies=self.cookie)
        logger.info(self.cookie)
        logger.info(r.text)
        # 如果名称已存在，删除后新增
        if r.json()['message'] == '项目名称已存在':
            sql = "delete from collection_project_approval where name='%s'"%(nproject['name'])
            self.db.delete_data(sql)
            print('delete same name productinfo')
            r = requests.post(url=url+'projectinfo/addProject', params=nproject, headers=header_json, cookies=self.cookie)
        self.assertEqual("新增成功", r.json()['message'])
        
    def test_f1_listproject(self):
        '获取项目id-定向'
        r = requests.post(url=url+'orientation/projectinfo/list', data={'page':1,'limit':100,'status':'','name':nproject['name']}, headers=header_json, cookies=self.cookie)
        print(r.text)
        oprojectsid = []
        for nprojects in r.json()['data']:
            oprojectsid.append(nprojects['id'])
        oprojectsid.sort(reverse = True)
        cdatas.oprojectid = oprojectsid[0]
        logger.info('定向项目id=%s'%oprojectsid[0])
        self.assertEqual(200, r.status_code)

    def test_f2_prostatus(self):
        '校验项目状态-定向'
        r = requests.post(url + 'orientation/projectinfo/viewProject', params={'id': cdatas.oprojectid}, headers=header_www, cookies=self.cookie)
        status = r.json()['data']['status']
        self.assertEqual(1, status)

if __name__ == '__main__':    
    # suit = unittest.TestSuite()
    # suit.addTest(Project('test_a0_gettee'))
    # # suit.addTest(Project('test_f1_listproject'))
    # # suit.addTest(Project('test_f2_prostatus'))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    unittest.main()