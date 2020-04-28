rem 启动locust服务，浏览器访问http://localhost:8089/，可以看到Locust WEB页面
rem 指定IP执行
rem locust -f locust_ztbiz.py --host=http://172.16.101.224:9200
rem  直接执行
locust -f locust_ztbiz.py
