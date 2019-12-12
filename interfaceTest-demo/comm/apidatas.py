'''
将api文档(swagger)转换成Excel
'''
import os
import re
import sys
import base64
import datetime
import time
fapath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(fapath)
import json
import requests
import unittest
import pandas
from openpyxl import Workbook
from comm.mysql import mysqlconnect
from comm.config import result_db, project_conf

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'doc')
url = 'http://172.16.101.224:9200'
nowtime = time.strftime("%Y-%m-%d %H:%M:%S")

total_message = []
def get_apiurl():
    '获取API接口数据'
    r = requests.get(url=url+'/swagger-resources')
    #print(r.json())
    names = {}
    total = 0   #接口数量
    for datas in r.json():
            name = datas['name']
            location = datas['location']
            name = name.split('-')
            name = name[0]
            if name == 'tebonx':
                continue
            message = [name, location]
            print(message)
            apidatas = get_api_doc(location)
            if apidatas != False:
                createsheet(apidatas, name)
                names[name] = len(apidatas)
                total += len(apidatas)
            else:
                continue
    print('本地落地的接口文件：',names)
    totalfile = os.path.join(path, 'total.txt')
    insertdb(total)
    with open(totalfile, 'a+') as f:
        f.write('当前统计时间：%s'%nowtime+'\n')
        f.write(str(names)+'\n')

def get_api_doc(apidoc):
    '获取的API接口数据'
    r = requests.get(url=url+apidoc)
    if r.status_code == 200:
        info = []
        respinfo = r.json()
        info = [respinfo['info']['description'], respinfo['info']['title'], respinfo['host'], respinfo['basePath']]
        resp = r.json()['paths']
        #print(paths)
        api_message = []
        api_message.append(info)
        for key in resp.keys():
                apipath = key   #接口地址
                print(apipath)
                apimethods = list(resp[key].keys())  #接口请求类型
                summarylist = []
                for apimethod in apimethods:
                    # print(apimethod)
                    summary=resp[key][apimethod]['summary'] #接口描述
                    tags = resp[key][apimethod]['tags'][0]  # 接口集合
                    # print(tags)
                    if summary not in summarylist:
                        summarylist.append(summary)
                    else:
                        break
                    # print(summary)
                message = [tags, apipath, apimethod, summary]
                print(message)
                api_message.append(message)
        return api_message
    else:
        return False

def createsheet(wtmessage, sheetname):
    '创建Excel并写入数据'
    filepath = os.path.join(path, sheetname+'.xlsx')
    df = pandas.DataFrame(wtmessage)
    with pandas.ExcelWriter(filepath) as f:
        df.to_excel(f, sheet_name=sheetname)

def insertdb(total):
    '将统计结果写入数据库'
    db = mysqlconnect(result_db.dbname)
    sql = "insert into %s (project, total, starttime) VALUES('%s', %s, '%s')"%(result_db.apitable, project_conf.project, total, nowtime)
    db.update_data(sql)
    print('数据库写入完成')

if __name__ == '__main__':
    # get_api_doc()
    get_apiurl()
    # createsheet()