'''
把对象作为函数
当对象可调用时（使用callable(funcname)测试是否可调用），
他们与函数一样，通过__call__方法实现
可用此方法实现数据库的初始化
'''

class Greeter:
   def __init__(self, greeting):
      self.greeting = greeting
   def __call__(self, name):
      return self.greeting + " " + name

morning = Greeter("good morning") #creates the callable object
morning("john") # calling the object
