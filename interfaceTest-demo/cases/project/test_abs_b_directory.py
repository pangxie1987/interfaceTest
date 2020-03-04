# -*- coding:utf-8 -*-
'''
文档管理接口

'''
import os
import sys
fapath = os.path.dirname(os.path.dirname(__file__))
fapath = os.path.join(fapath, '../')
sys.path.append(fapath)
import requests
import unittest
from urllib3 import encode_multipart_formdata
from comm.readjson import read
from comm.mysql import mysqlconnect
from comm.commdata import cdatas

url = read('commdata.json')['url']
directory = read('directory.json')['directory']
header_www = read('headers.json')['header_www']
header_json = read('headers.json')['header_json']


# 项目默认目录-标准
directoryname = ['立项会', '资产管理委员会', '投决会',
'产品法律文件', '产品发行', '验资成立', '产品备案', '账户资料', '投资运作', 
'产品清盘', '其它', '立项会会议附件', '立项会会议结果附件', '资产管理委员会会议附件',
 '资产管理委员会会议结果附件','投决会会议附件', '投决会会议结果附件', '销售公告',
 '销售要素确认通知单', '募集结束公告', '备案材料', '备案报告', '托管户相关材料', '股东户相关材料',
 '基金户相关材料', '银行间债券户相关材料','期货户相关材料', '其它户相关材料', 
 '存续期公告', '资产管理报告', '指令类单据', '交易类单据', '资金类单据', '流程类单据',
 '其他存续期资料', '季报', '半年报', '年报', '投资指令', '划款指令','代销','代销相关协议、准入文件']

# 项目默认目录-非标
directoryname1 = ['产品法律文件', '产品发行', '验资成立', '产品备案', '账户资料', '投资运作', '产品清盘', 
'其它', '接洽材料', '尽调','立项会', '资产管理委员会', '投决会', '尽调材料', '尽调报告', 
'立项会会议附件', '立项会会议结果附件', '资产管理委员会会议附件', '资产管理委员会会议结果附件', 
'投决会会议结果附件', '投决会会议附件', '销售公告', '销售要素确认通知单', '募集结束公告', '备案材料', '备案报告',
'托管户相关材料', '股东户相关材料', '基金户相关材料', '银行间债券户相关材料',
'期货户相关材料', '其它户相关材料', '存续期公告', '资产管理报告', '指令类单据', '交易类单据', 
'资金类单据', '流程类单据', '其他存续期资料', '季报', '半年报', '年报', '投资指令', '划款指令','代销','代销相关协议、准入文件']

# 项目默认目录-定向
directoryname2 = ['接洽材料', '尽调', '立项会', '资产管理委员会', '投决会', '产品法律文件', 
'产品备案', '起始运作', '账户资料', '投资运作', '产品清盘', '其它', '尽调材料', '尽调报告', 
'立项会会议附件', '立项会会议结果附件', '资产管理委员会会议附件', '资产管理委员会会议结果附件', 
'投决会会议附件', '投决会会议结果附件', '备案材料', '备案报告', '产品起始运作通知书', 
'其他起始运作材料', '托管户相关材料', '股东户相关材料', '基金户相关材料', '银行间债券户相关材料',
'期货户相关材料', '其它户相关材料', '资产管理报告', '指令类单据', '交易类单据',
'资金类单据', '流程类单据', '其他存续期资料', '季报', '半年报', '年报', '投资指令', '划款指令', '追加/提取通知书']

class FileTree(unittest.TestCase):
    '文档管理'
    
    @classmethod
    def setUp(self):
        self.db = mysqlconnect('zgcollection')

    @classmethod
    def setUpClass(self):
        self.cookie = read('cookies.json')

    @classmethod
    def tearDownClass(self):
        self.db.closedb()

    def test_a_table(self):
        '获取左侧目录列表-标准'
        r = requests.post(url=url+'document/table', data={"projectId":cdatas.projectid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        name_list = []
        for names in r.json():
            name_list.append(names['name'])
        print(name_list)
        name_list.sort()
        directoryname.sort()
        self.assertEqual(name_list, directoryname)

    def test_b0_add_node(self):
        '目录新增节点-子节点'
        
        sql = "select id from collection_project_directory where name = '立项会会议附件' and project_id = %s"%(cdatas.projectid)
        FileTree.cailiaoid = self.db.execute(sql)[0]
        directory['id'] = FileTree.cailiaoid
        directory['name'] = "Word_A"
        directory['isChild'] = 1    #材料制作子节点0-同级节点，1-子节点
        directory['isEnd'] =0   # 在isChild=0时0-排序最前，1-排序最后,isChild=1时，总是排在最后
        directory['fileId'] =''

        r = requests.post(url=url+'document/add_node', data=directory, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])

    def test_b1_table(self):
        '目录新增节点-子节点-验证'
        r = requests.post(url=url+'document/table', data={"projectId":cdatas.projectid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        for names in r.json():
            if names['name'] == directory['name']:
                nodepid = names['pid']  # 获取父节点
                break
        # 新增子节点，验证父节点
        self.assertEqual(nodepid, directory['id'])

    def test_c0_add_node(self):
        '目录新增节点-同级节点-排序最前'
        sql = "select id from collection_project_directory where name = '资产管理委员会会议附件' and project_id = %s"%(cdatas.projectid)
        FileTree.wordid = self.db.execute(sql)[0]
        directory['id'] = FileTree.wordid
        directory['name'] = "Excel"
        directory['isChild'] = 0    #材料制作子节点0-同级节点，1-子节点
        directory['isEnd'] =0   # 在isChild=0时0-排序最前，1-排序最后,isChild=1时，总是排在最后
        directory['fileId'] =''
        r = requests.post(url=url+'document/add_node', data=directory, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])

    def test_c1_table(self):
        '目录新增节点-同级节点-排序最前-验证'
        print(directory)
        r = requests.post(url=url+'document/table', data={"projectId":cdatas.projectid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        for names in r.json():
            if names['name'] == directory['name']:
                nodenum = names['num']  # 节点的排序顺序
                break
        self.assertEqual(0, nodenum)

    def test_d0_add_node(self):
        '目录新增节点-同级节点-排序最后'
        directory['id'] = FileTree.wordid
        directory['name'] = "Word1"
        directory['isChild'] = 0    #材料制作子节点0-同级节点，1-子节点
        directory['isEnd'] =1   # 在isChild=0时0-排序最前，1-排序最后,isChild=1时，总是排在最后
        directory['fileId'] =''
        r = requests.post(url=url+'document/add_node', data=directory, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])

    def test_d1_table(self):
        '目录新增节点-同级节点-排序最后-验证'
        r = requests.post(url=url+'document/table', data={"projectId":cdatas.projectid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        for names in r.json():
            if names['name'] == directory['name']:
                nodenum = names['num']  # 节点的排序顺序
                FileTree.nodeins = names['id']   # 新增节点的id
                FileTree.nodepid = names['pid']    #父节点id
                print(FileTree.nodeins)
                break
        # 统计父节点下，子节点的数量
        sql = 'select count(*) from collection_project_directory where pid = %s'%(FileTree.nodepid)
        count = self.db.execute(sql)[0]
        # self.assertEqual(count, nodenum)
        self.assertEqual(2, nodenum)

    def test_e1_updatebyid(self):
        '修改节点'
        updatedata = {"id":1,"name":'',"remark":''}
        updatedata['id'] = FileTree.nodeins
        updatedata['name'] = directory['name']
        updatedata['remark'] = 'update-directory'
        r = requests.post(url=url+'document/updateById', data=updatedata, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])

    def test_e2_complete(self):
        '标记完成'
        r = requests.post(url=url+'document/complete', data={'id':FileTree.nodeins,compile:0}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual('操作成功', r.json()['message'])

    def test_e3_updatebyid(self):
        '修改节点-修改标记完成的节点'
        updatedata = {"id":1,"name":'',"remark":''}
        updatedata['id'] = FileTree.nodeins
        updatedata['name'] = directory['name']
        updatedata['remark'] = 'update-directory'
        r = requests.post(url=url+'document/updateById', data=updatedata, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])

    def test_e4_complete(self):
        '去标记'
        r = requests.post(url=url+'document/complete', data={'id':FileTree.nodeins,compile:1}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual('操作成功', r.json()['message'])

    def test_e5_complete(self):
        '再次标记'
        r = requests.post(url=url+'document/complete', data={'id':FileTree.nodeins,compile:0}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual('操作成功', r.json()['message'])

    def test_g0_upload(self):
        '上传文件-docx格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testfile.docx')
        filedata['file'] = ('testfile.docx', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])

    def test_g1_listChildren(self):
        '获取右侧文件列表'
        r = requests.post(url=url+'document/listChildren', data={'page':1,'limit':100,'id':FileTree.nodepid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        FileTree.docxid = r.json()['data'][0]['id'] #获取文件id
        FileTree.fileId = r.json()['data'][0]['fileId'] #获取文件fileid
        self.assertEqual(1, r.json()['count'])

    def test_g2_download(self):
        '下载文件-docx'
        sql = 'select file_server_id from collection_product_file where id =%s'%(FileTree.fileId)
        downfileid = self.db.execute(sql)[0]
        r = requests.post(url=url+'file/download', data={'fileId':downfileid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual(200, r.status_code)  

    def test_g3_delete(self):
        '删除节点-docx'
        r = requests.post(url=url+'document/delete', data={'id':(FileTree.docxid)}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])    

    def test_h0_upload(self):
        '上传文件-xlsx格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'接口测试OA上传文件.xlsx')
        filedata['file'] = (u'接口测试OA上传文件.xlsx', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])

    def test_h1_listChildren(self):
        '获取右侧文件列表'
        r = requests.post(url=url+'document/listChildren', data={'page':1,'limit':100,'id':FileTree.nodepid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        FileTree.docxid = r.json()['data'][0]['id'] #获取文件id
        FileTree.fileId = r.json()['data'][0]['fileId'] #获取文件fileid
        self.assertEqual(1, r.json()['count'])

    def test_h2_download(self):
        '下载文件-xlsx'
        sql = 'select file_server_id from collection_product_file where id =%s'%(FileTree.fileId)
        downfileid = self.db.execute(sql)[0]
        r = requests.post(url=url+'file/download', data={'fileId':downfileid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual(200, r.status_code)  

    def test_h3_delete(self):
        '删除节点-xlsx'
        r = requests.post(url=url+'document/delete', data={'id':(FileTree.docxid)}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])

    def test_j0_upload(self):
        '上传文件-txt格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testfile.txt')
        filedata['file'] = ('testfile.txt', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("该上传文件格式不允许上传", r.json()['message'])

    # def test_j1_listChildren(self):
    #     '获取右侧文件列表'
    #     r = requests.post(url=url+'document/listChildren', data={'page':1,'limit':100,'id':FileTree.nodepid}, headers=header_www, cookies=self.cookie)
    #     print(r.text)
    #     FileTree.docxid = r.json()['data'][0]['id'] #获取文件id
    #     FileTree.fileId = r.json()['data'][0]['fileId'] #获取文件fileid
    #     self.assertEqual("1", r.json()['count'])

    # def test_j2_download(self):
    #     '下载文件-txt'
    #     r = requests.post(url=url+'file/download', data={'fileId':(FileTree.fileId)}, headers=header_www, cookies=self.cookie)
    #     print(r.text)
    #     self.assertEqual(200, r.status_code)    

    # def test_j3_delete(self):
    #     '删除节点'
    #     r = requests.post(url=url+'document/delete', data={'id':(FileTree.docxid)}, headers=header_www, cookies=self.cookie)
    #     print(r.text)
    #     self.assertEqual("操作成功", r.json()['message'])

    def test_k0_upload(self):
        '上传文件-pdf格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'ApacheFlink.pdf')
        filedata['file'] = ('ApacheFlink.pdf', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])

    def test_k1_listChildren(self):
        '获取右侧文件列表'
        r = requests.post(url=url+'document/listChildren', data={'page':1,'limit':100,'id':FileTree.nodepid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        FileTree.docxid = r.json()['data'][0]['id'] #获取文件id
        FileTree.fileId = r.json()['data'][0]['fileId'] #获取文件fileid
        self.assertEqual(1, r.json()['count'])

    def test_k2_download(self):
        '下载文件-pdf'
        sql = 'select file_server_id from collection_product_file where id =%s'%(FileTree.fileId)
        downfileid = self.db.execute(sql)[0]
        r = requests.post(url=url+'file/download', data={'fileId':downfileid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual(200, r.status_code)   

    def test_k3_delete(self):
        '删除节点-pdf'
        r = requests.post(url=url+'document/delete', data={'id':(FileTree.docxid)}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])

    def test_kk0_upload(self):
        '上传文件-已损坏文件'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'sunhuai.xlsx')
        filedata['file'] = ('sunhuai.xlsx', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])

    def test_kk1_listChildren(self):
        '获取右侧文件列表'
        r = requests.post(url=url+'document/listChildren', data={'page':1,'limit':100,'id':FileTree.nodepid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        FileTree.docxid = r.json()['data'][0]['id'] #获取文件id
        FileTree.fileId = r.json()['data'][0]['fileId'] #获取文件fileid
        self.assertEqual(1, r.json()['count'])

    def test_kk2_download(self):
        '下载文件-已损坏文件'
        sql = 'select file_server_id from collection_product_file where id =%s'%(FileTree.fileId)
        downfileid = self.db.execute(sql)[0]
        r = requests.post(url=url+'file/download', data={'fileId':downfileid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual(200, r.status_code)   

    def test_kk3_delete(self):
        '删除节点-已损坏文件'
        r = requests.post(url=url+'document/delete', data={'id':(FileTree.docxid)}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("操作成功", r.json()['message'])

    def test_l0_upload(self):
        '上传文件-csv格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testcsv.csv')
        filedata['file'] = ('testcsv.csv', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message']) 

    def test_l1_upload(self):
        '上传文件-doc格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testdoc.doc')
        filedata['file'] = ('testdoc.doc', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message']) 

    def test_l2_upload(self):
        '上传文件-ppt格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testppt.ppt')
        filedata['file'] = ('testppt.ppt', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])

    def test_l3_upload(self):
        '上传文件-pptx格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testpptx.pptx')
        filedata['file'] = ('testpptx.pptx', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])   

    def test_l4_upload(self):
        '上传文件-xls格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testxls.xls')
        filedata['file'] = ('testxls.xls', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])

    def test_l5_upload(self):
        '上传文件-bmp格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testbmp.bmp')
        filedata['file'] = ('testbmp.bmp', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message']) 

    def test_l6_upload(self):
        '上传文件-jpeg格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testjpeg.jpeg')
        filedata['file'] = ('testjpeg.jpeg', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])

    def test_l7_upload(self):
        '上传文件-jpg格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testjpg.jpg')
        filedata['file'] = ('testjpg.jpg', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message'])   

    def test_l8_upload(self):
        '上传文件-png格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'testpng.png')
        filedata['file'] = ('testpng.png', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("操作成功", r.json()['message']) 

    def test_m0_upload(self):
        '上传文件-不支持的格式'
        filedata = {"pid":FileTree.nodepid,"file":"1"}
        namepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downfile\\'+'EConnect.vbs')
        filedata['file'] = ('EConnect.vbs', open(namepath,'rb').read())
        encode_data = encode_multipart_formdata(filedata)
        filedata = encode_data[0]
        header = {'Content-Type':'1'}
        header['Content-Type'] = encode_data[1]
        r = requests.post(url=url+'document/upload', data=filedata, headers=header, cookies=self.cookie)
        print(r.text)   # 如果添加成功，r.text = '1'
        self.assertEqual("该上传文件格式不允许上传", r.json()['message'])

    def test_m1_delete(self):
        '删除目录节点'
        r = requests.post(url=url+'document/delete', data={'id':(FileTree.nodepid)}, headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual("该目录不能修改", r.json()['message'])         

    def test_n_tree(self):
        '获取树形目录结构'
        r = requests.post(url=url+'document/tree', data={"projectId":cdatas.projectid},headers=header_www, cookies=self.cookie)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_p_search(self):
        '文件查询'
        r = requests.post(url=url+'document/listChildren', data={'page':1,'limit':'300','id':1542}, headers=header_www, cookies=self.cookie)
        print(r.text)
        sql = 'select count(*) from collection_project_directory where pid=1542'
        count = self.db.execute(sql)[0]
        self.assertEqual(count, r.json()['count'])

    def test_q1_table(self):
        '获取左侧目录列表-非标'
        r = requests.post(url=url+'document/table', data={"projectId":cdatas.nprojectid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        name_list = []
        for names in r.json():
            name_list.append(names['name'])
        print(name_list)
        name_list.sort()
        directoryname1.sort()
        self.assertEqual(name_list, directoryname1)

    def test_q2_table(self):
        '获取左侧目录列表-定向'
        r = requests.post(url=url+'document/table', data={"projectId":cdatas.oprojectid}, headers=header_www, cookies=self.cookie)
        print(r.text)
        name_list = []
        for names in r.json():
            name_list.append(names['name'])
        print(name_list)
        name_list.sort()
        directoryname2.sort()
        print(directoryname2.sort())
        print(name_list.sort())
        self.assertEqual(name_list, directoryname2)

if __name__ == '__main__':
    unittest.main()
    # suit = unittest.TestSuite()
    # # suit.addTest(FileTree('test_c0_add_node'))
    # # suit.addTest(FileTree('test_c1_table'))
    # # suit.addTest(FileTree('test_d_listChildren'))
    # suit.addTest(FileTree('test_q2_table'))

    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    