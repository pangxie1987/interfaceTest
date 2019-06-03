'''
对数据进行格式化处理
'''

import os
filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'productinfo.txt')
data_dict = []
f = open (filepath)
datas = f.read()
#print(datas)
datas = datas.split('&')
for data in datas:
    data = data.replace('=',':')
    print(data)


# for data in datas:
#     data_dict.append(data)
# print(data_dict)