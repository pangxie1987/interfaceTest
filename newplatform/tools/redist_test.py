# redis批量插入数据
# https://testerhome.com/topics/25448
import redis
r = redis.Redis(host='172.16.101.223', port='6379', db=0)
print(r)
