rem 启动locust服务，浏览器访问http://localhost:8089/，可以看到Locust WEB页面
locust -f locust_ztbiz.py --host=http://172.16.101.224:9200