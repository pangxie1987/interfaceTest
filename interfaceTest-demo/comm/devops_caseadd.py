import os
import sys
fapath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(fapath)
import requests
from comm.logset import logger
# from comm.gettoken import usertokenbyurl
from comm.config import result_devops as devops

def usertokenbyurl(username, password, gateway, client_id, client_secret):
    '''
    获取用户名密码获取token
    gateway:系统gateway地址
    client_id:
    client_secret:
    '''
    headers={
        "Authorization": "1222",
        "client_id": client_id,
        "client_secret": client_secret
        }

    mytoken = {"Authorization":""}
    r = requests.post(url=gateway+'/api-auth/oauth/user/token',  data={"username":username, "password":password}, headers=headers)
    mytoken['Authorization'] = "Bearer " + r.json()['access_token']
    logger.info(mytoken)
    return mytoken


def devopscase_add(caseinfo):
    '将接口自动化测试案例插入devops中'
    token = usertokenbyurl(devops.username,devops.mypasswd,devops.gateway,devops.client_id,devops.client_secret)
    headers = token
    r = requests.post(url=devops.gateway+'/api-devops/testCase/importAutoTestcaseData', json=caseinfo, headers=headers)
    logger.info(r.text)
    
if __name__ == '__main__':
    devopscase_add('')
