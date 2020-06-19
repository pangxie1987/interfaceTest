'''
装饰器学习
没看完这11 条，别说你精通 Python 装饰器
https://mp.weixin.qq.com/s?__biz=MzU1OTI0NjI1NQ==&mid=2247485460&idx=1&sn=199c47871ad94c857b652fcc130b2684&chksm=fc1b76d4cb6cffc2032adf952ad3ec163841bd38a10e84944b3355f90301d6d756c258c3541f&scene=126&sessionid=1591748565&key=46ed05c0f8d512c3487568bd43a8ced9b2d56c04c2f598c7509a2f9fdce3577e8946daf3f7e55240af35ae9dea6101c8bf539fbd0e37d33132bbdb7f540faea19b821ee64b8dd4e46fa82333c68ab05b&ascene=1&uin=MjU1MjExMjgxNw%3D%3D&devicetype=Windows+7+x64&version=62090070&lang=zh_CN&exportkey=AfbLRT9QXUmDIr0t9Us0sm4%3D&pass_ticket=ctsSf6tr20Kt5CIzrBXM%2F8xXg9UqDXil71YlSu9gJvDkEEF9PFw3HV%2FBkKk2J85O

'''

import time
import requests


# -------------1、Hello,装饰器-------------

def decorator(func):
	def wrapper(*args, **kwargs):
		return func
	return wrapper

@decorator
def function():
	print('hello, decorator')

# -------------2、入门：日志打印-------------
def lgger(func):
	'打印日志'
	def wrapper(*args, **kwargs):
		print('执行函数：{}'.format(func.__name__))
		func(*args, **kwargs)
		print('执行完成')
	return wrapper

@lgger
def add(x, y):
	print('{}+{}={}'.format(x, y, x+y))

# -------------3、入门：时间计时器-------------
def timer(func):
	'计算函数执行时间'
	def wrapper(*args, **kwargs):
		t1 = time.time()
		func(*args, **kwargs)
		t2 = time.time()
		cost_time = t2-t1
		print('花费时间：{}秒'.format(cost_time))
	return wrapper

@timer
def want_sleep(sleep_time):
	# time.sleep(sleep_time)
	r = requests.get(url='http://www.baidu.com')
	print(r.text)

# -------------4、进阶：带参数的函数装饰器-------------
def say_hello(country):
	'''
	带参数的装饰器
	根据国籍打招呼
	'''
	def wrapper(func):
		def deco(*args, **kwargs):
			if country == 'china':
				print('你好')
			elif country == 'america':
				print('hello')
			else:
				return 

			func(*args, **kwargs)
		return deco
	return wrapper

@say_hello('china')
def xiaoming():
	pass

@say_hello('america')
def jack():
	pass


# -------------5、高阶：不带参数的类装饰器-------------
class Logger(object):
	'基于类不带参数的装饰器'
	def __init__(self, func):
		'接收被装饰函数'
		self.func = func

	def __call__(self, *args, **kwargs):
		'实现装饰逻辑'
		print("[INFO]: the function {func}() if running....".format(func=self.func.__name__))
		return self.func(*args, **kwargs)

@Logger
def say(something):
	print("say {}!".format(something))


# -------------6、高阶：带参数的类装饰器-------------	

class Loggerargs(object):
	'带参数的类装饰器'
	def __init__(self, level='INFO'):
		'接收传入参数'
		self.level = level

	def __call__(self, func):
		'接收装饰函数，实现装饰逻辑'
		def wrapper(*args, **kwargs):
			print("[{level}]: the function {func}() is running...".format(level=self.level, func=func.__name__))
			func(*args, **kwargs)
		return wrapper

@Loggerargs(level="Error")
def say2(something):
	print("say {}".format(something))


# ------------7、使用偏函数与类实现装饰器-------------
import functools

class DelayFunc:
	'''
	实现一个__call__的类，从而这个类可以callable
	'''
	def __init__(self, duration, func):
		self.duration = duration
		self.func = func

	def __call__(self, *args, **kwargs):
		print(f'wait for {self.duration} seconds...')
		time.sleep(self.duration)
		return self.func(*args, **kwargs)

	def eager_call(self, *args, **kwargs):
		print('Call without delay')
		return self.func(*args, **kwargs)


def delay(duration):
	'''
	装饰器：推迟某个函数的执行
	同时提供.eager_call方法立即执行
	'''
	# 此处为了避免定义额外函数，直接使用functools.partial(DelayFunc, duration)
	return functools.partial(DelayFunc, duration)

@delay(duration=2)
def add_delay(a, b):
	return a+b

# --------------8、能装饰类的装饰器-------------
instances = {}
def singleton(cls):
	'实现能装饰类的装饰器'
	def get_instance(*args, **kwargs):
		cls_name = cls.__name__
		print('====1====')
		if not cls_name in instances:
			print('====2====')
			instance = cls(*args, **kwargs)
			instances[cls_name] = instance
			print(instances)
		return instances[cls_name]
	return get_instance

@singleton
class User:
	_instance = None

	def __init__(self, name):
		print('====3====')
		self.name = name


# --------------9、wraps装饰器作用---------------
from functools import wraps
'''
方法是使用 functools .wraps 装饰器，
它的作用就是将 被修饰的函数(wrapped) 的一些属性值赋值给 修饰器函数(wrapper) ，
最终让属性的显示更符合我们的直觉
'''
def wrapper(func):
	@wraps(func)
	def inner_function():
		pass
	return inner_function

@wrapper
def wrapped():
	pass

# --------------10、内置装饰器：property---------------

class Student(object):
	'''
	用@property装饰过的函数，会将一个函数定义成一个属性，
	属性的值就是该函数return的内容。同时，会将这个函数变成另外一个装饰器。
	就像后面我们使用的@age.setter和@age.deleter。
	'''
	def __init__(self, name):
		self.name = name
		self.name = None
	@property
	def age(self):
		return self._age

	@age.setter
	def age(self, value):
		if not isinstance(value, int):
			raise ValueError('输入不合法：年龄必须为整数')
		if not 0< value <100:
			raise ValueError('输入不合法：年龄范围必须0-100')
		self._age=value
	@age.deleter
	def age(self):
		del self._age


# --------------11、装饰器实战：控制函数超时时间---------------
# linux方法，等待函数超时
import signal
class TimeoutException(Exception):
	def __init__(self, error='Timeout wating for response from Cloud'):
		Exception.__init__(self, error)

def timeout_limit(timeout_time):
	def wraps(func):
		def handler(signum, frame):
			raise TimeoutException()

		def deco(*args, **kwargs):
			signal.signal(signal.SIGALRM, handler)
			signal.alarm(timeout_time)
			func(*args, **kwargs)
			signal.alarm(0)
		return deco
	return wraps

@timeout_limit(1)
def waitout(time_limit):
	time.sleep(time_limit)
	print('waitout run sucesss!')



if __name__ == '__main__':
	# add(4,5)
	# want_sleep(5)
	# xiaoming()
	# jack()
	# say('nihao')
	# say2('test')
	# add_delay(1,4)

	# u1 = User('wang')
	# u1.age = 20
	# u2 = User('wang2')
	# print(u2.age)

	# waitout(3)
	# print(wrapped.__name__)
	xiaoming = Student('小明')
	# 设置属性
	xiaoming.age = 11
	# 查询属性
	print(xiaoming.age)
	# 删除属性
	del xiaoming.age
