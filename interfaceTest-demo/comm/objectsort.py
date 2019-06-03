# -*- coding:utf-8 -*-
'''
数据类型处理
'''

def tuple2list(mytuple):
    '将元素数据转换成列表'
    if mytuple == None:
        print('元组为空，不可转换成列表!!!')
        newlist = mytuple
    elif len(mytuple) == 0:
        print('元组中没有元素，不可转换成列表!!!')
        newlist = mytuple
    elif len(mytuple) == 1:
        print('元组中只有一个元素')
        newlist = [mytuple[0]]
    else:
        newlist = [i[0] for i in mytuple]
    
    return newlist

def sort_up(mylist):
    '对列表进行升序排序'
    mylist.sort(reverse = False)
    return mylist

def sort_down(mylist):
    '对列表进行降序排序'
    mylist.sort(reverse = True)
    return mylist

if __name__ == '__main__':
    # a = (('a'), ('c'), ('b'))

    # b = ['c', 'a', 'b']

    # a = tuple2list(a)
    # a = sort_up(a)
    # print(a)
    # b = sort_up(b)
    # if a == b:
    #     print('OK')
    a = (('a'),)
    print(tuple2list(a))