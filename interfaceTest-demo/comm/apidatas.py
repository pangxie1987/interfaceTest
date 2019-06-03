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

cookie = read('cookies.json')
path = os.path.dirname(os.path.dirname(__file__))
apifile = os.path.join(path, "report\\"+"mobile.xlsx")

exceltile = ['接口集合名称','接口地址','接口请求类型','接口描述']

collection = 'http://172.16.100.22:6002/v2/api-docs'    #集合+abs接口地址
notice = 'http://172.16.100.22:9016/v2/api-docs'        #消息推送接口地址

def get_api_doc():
    'api文档数据转换'
    r = requests.get(url=collection, cookies=cookie)
    resp = r.json()['paths']
    all_message = []
    for key in resp.keys():
        
        apipath = key   #接口地址
        print(apipath)
        #print(list(resp[key].keys())[0])
        apimethod = list(resp[key].keys())[0]  #接口请求类型
        print(apimethod)
        summary=resp[key][apimethod]['summary'] #接口描述
        print(summary)
        tags = resp[key][apimethod]['tags'][0]
        message = [tags, apipath, apimethod, summary]
        all_message.append(message)
        df = pandas.DataFrame(all_message)
        df.to_excel(apifile)    #写入Excel

if __name__ == '__main__':
    get_api_doc()
