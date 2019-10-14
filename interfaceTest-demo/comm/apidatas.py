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
from comm.readjson import read
from openpyxl import Workbook

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'doc')
url = 'http://172.16.101.224:9200'

total_message = []
def get_apiurl():
    '获取API接口数据'
    r = requests.get(url=url+'/swagger-resources')
    #print(r.json())
    names = {}
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
            else:
                continue
    print('本地落地的接口文件：',names)
    totalfile = os.path.join(path, 'total.txt')
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
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

if __name__ == '__main__':
    # get_api_doc()
    get_apiurl()
    # createsheet()