'''
远程Linux执行shell命令
https://www.jb51.net/article/132770.htm
https://www.cnblogs.com/pymkl/articles/9184737.html
'''
import os
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
    
    def sftp(self, localfile, remotepath):
        'sftp服务，创建或者传输文件'
        print('---------------- start put files:{} ----------------'.format(localfile))
        sftp = self.client.open_sftp()
        # 创建目录
        # sftp.mkdir('abc')
        # 从远程主机下载文件，如果失败， 这个可能会抛出异常。
        # sftp.get('test.sh', '/home/testl.sh')
        # sftp.get(remotepath, localfile)
        # 上传文件到远程主机，也可能会抛出异常
        sftp.put(localfile, remotepath)
    
def commnd():
    myclient = paramiko.SSHClient()
    # 设置成默认自动接受密钥
    myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接远程主机
    myclient.connect("172.16.101.225", port=22, username="root", password="tebon2017")
    # 在远程机执行shell命令
    stdin, stdout, stderr = myclient.exec_command("ls -l")
    # 读返回结果
    print (stdout.read())
    # 在远程机执行python脚本命令
    stdin, stdout, stderr = myclient.exec_command("ls")

def wincmd(cmd):
    '''
    执行Windows命令
    path: 要执行命令的目录
    cmd: 要执行的命令
    '''
    return os.system(cmd)

if __name__ == '__main__':
    wincmd('git pull')  # 拉取代码
    wincmd('mvn clean install -U -T 1C -Dmaven.test.skip=true -Dmaven.compile.fork=true')   # 编译
    ssh = SSH('172.16.105.99', 'root', 'tebon@2019')    # 连接服务器
    ssh.ssh_shell('ls -a')
    ssh.sftp('./target/tebonx-cloud-ztbiz-server.war', '/root/war_bak/ztbiz-server/tebonx-cloud-ztbiz-server.war')   # 上传文件
    ssh.ssh_shell('sh /root/war_bak/ztbiz-server/update_war.sh')  # 启动服务
    