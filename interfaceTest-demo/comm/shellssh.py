'''
远程Linux执行shell命令
https://www.jb51.net/article/132770.htm
https://www.cnblogs.com/pymkl/articles/9184737.html
'''

import paramiko

class SSH(object):
    '创建ssh连接'
    def __init__(self, sys_ip, username, passwd):
        try:
            self.client = paramiko.SSHClient()
            # 设置成默认自动接受密钥
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(sys_ip, 22, username=username, password=passwd, timeout=20)
        except Exception as e:
            print(e)
        # finally:
        #     self.client.close()

    def ssh_shell(self, cmds):
        '执行shell命令'
        stdin, stdout, stderr = self.client.exec_command(cmds)
        result = stdout.readlines()
        print(result)
        return result
        self.client.close()
    
    def sftp(self, cmds):
        'sftp服务，创建或者传输文件'
        sftp = self.client.open_sftp()
        # 创建目录
        sftp.mkdir('abc')
        # 从远程主机下载文件，如果失败， 这个可能会抛出异常。
        sftp.get('test.sh', '/home/testl.sh')
        # 上传文件到远程主机，也可能会抛出异常
        sftp.put('/home/test.sh', 'test.sh')
    
def commnd():
    myclient = paramiko.SSHClient()
    # 设置成默认自动接受密钥
    myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接远程主机
    myclient.connect("172.16.100.22", port=22, username="root", password="tebon2017")
    # 在远程机执行shell命令
    stdin, stdout, stderr = myclient.exec_command("ls -l")
    # 读返回结果
    print (stdout.read())
    # 在远程机执行python脚本命令
    stdin, stdout, stderr = myclient.exec_command("ls")

if __name__ == '__main__':
    ssh = SSH('172.16.100.20', 'root', 'tebon2017')
    ssh.ssh_shell('sh /usr/zgcollection-mobile/start-h5.sh')