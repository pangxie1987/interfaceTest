# coding: utf-8
'''
es数据导出
https://testerhome.com/topics/24884
'''

import json
import os
import time
import requests


class exportEsData():
    size = 10000
    def __init__(self, url,index,type):
        self.url = url+"/"+index+"/"+type+"/_search"
        self.urlput=url+"/"+index+"/_settings"
        self.index = index
        self.type = type
    def exportData(self):
        print("export data begin...")
        # puthead={"Content-Type": "application/json"}
        # param={ "index.max_result_window" :"1000000"}   #修改index max_result_window数据超过100万，一般是根据实际情况，进行修改
        # pload=json.dumps(param)
        # requests.put(url=self.urlput,data=pload,headers=puthead)
        begin = time.time()
        try:
            os.remove(self.index+"_"+self.type+".json")
        except:
            pass
        msg = requests.get(self.url).text
        print(msg)
        obj = json.loads(msg)
        num = obj["hits"]["total"]
        print(num)
        start = 0
        end =  num/self.size+1
        while(start<end):
            msg =requests.get(self.url+"?from="+str(start*self.size)+"&size="+str(self.size)).text
            print("msg_data=",msg)
            self.writeFile(msg)
            start=start+1
        print("export data end!!!\n\t total consuming time:"+str(time.time()-begin)+"s")
    def writeFile(self,msg):
        obj = json.loads(msg)
        vals = obj["hits"]["hits"]
        try:
            f = open(self.index+"_"+self.type+".json","a")
            for val in vals:
                a = json.dumps(val["_source"],ensure_ascii=False)
                f.write(a+"\n")
        finally:
            f.flush()
            f.close()


if __name__ == '__main__':
    # exportEsData("http://ip:port","index","type").exportData() #ip,port,index,type根据实际情况替换
    exportEsData("http://172.16.101.212:9200","i_secu_pool_kj","SECU_POOL_KJ").exportData() #ip,port,index,type根据实际情况替换