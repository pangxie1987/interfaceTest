# coding: utf-8
'''
es数据导入
https://testerhome.com/topics/24
'''
from elasticsearch import Elasticsearch
import json
import requests
from elasticsearch import helpers

class importEsData():
    def  __init__(self,url,index,type):
        self.url = url
        self.urlputindex=url+"/"+index
        self.urlputmapping=url+"/"+index+"/"+type+"/_mapping"
        self.index = index
        self.type = type
    def importData(self):
        es=Elasticsearch(self.url)
        requests.put(self.urlputindex)  #创建index
        param={mappings}    #这个可以用 http://ip:port/index 获取mappings 来替换mappings内容
        pload=json.dumps(param)
        requests.put(self.urlputmapping,pload)   #创建mappings

        actions=[]  #收集性能数据集合
        f = open(self.index+"_"+self.type+".json",encoding='gbk')

        while 1:
            line=f.readline()
            if not line:
                break
            lined=json.loads(line.encode())
            properties=lined["properties"]   #properties根据实际数据进行替换
            action = {
                    "_index": self.index,
                    "_type": self.type,
                    "_source": {
                        'properties': properties  #properties根据实际数据进行替换
                    }
                }
            actions.append(action)
            if len(actions)==10000:
                helpers.bulk(es, actions)
                del actions[0:len(actions)]
        f.close()
        helpers.bulk(es, actions)

if __name__ == '__main__':
    importEsData("http://ip:port","index","type").importData()  #ip,port,index,type根据实际情况替换