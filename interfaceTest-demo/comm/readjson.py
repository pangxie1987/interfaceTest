# -*- coding:utf-8 -*-
'''
读取json格式的文件
'''
import os
import json

def read(filename):
    '读取json文件'
    # 数据文件路径
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datas\\"+filename)
    datapath = os.path.abspath(path)

    # 解析json文件
    try:
        with open(datapath, encoding='utf-8') as f:
            datas = json.load(f)
            # print(datas)
        return datas
    except FileNotFoundError:
        print('%s不存在，请检查'%filename)

if __name__ == '__main__':
    mycoo = read('tb1.json')
    print(mycoo)
