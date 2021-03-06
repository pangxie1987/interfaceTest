'''
远程Linux执行shell命令
https://www.jb51.net/article/132770.htm
https://www.cnblogs.com/pymkl/articles/9184737.html
https://blog.csdn.net/littleRpl/article/details/90065836    # 文件目录上传下载
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

    def sftp_get(self, remotepath, localfile):
        '下载文件'
        sftp = self.client.open_sftp()
        sftp.get(remotepath, localfile)
        print('下载完成：{}'.format(remotepath))
    
    def sftp_put(self, localfile, remotepath):
        'sftp服务，创建或者传输文件'
        print('---------------- start put files:{} ----------------'.format(localfile))
        sftp = self.client.open_sftp()
        # 创建目录
        # sftp.mkdir('abc')
        sftp.put(localfile, remotepath)
        print('上传完成：{}'.format(remotepath))

    def __get_all_files_in_local_dir(self, local_dir):
        '获取本地指定目录及其子目录下的所有文件'
        all_files = list()
 
         # 获取当前指定目录下的所有目录及文件，包含属性值
        files = os.listdir(local_dir)
        for x in files:
            # local_dir目录中每一个文件或目录的完整路径
            filename = os.path.join(local_dir, x)
            # 如果是目录，则递归处理该目录
            if os.path.isdir(x):
                all_files.extend(self.__get_all_files_in_local_dir(filename))
            else:
                all_files.append(filename)
        return all_files
    
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
    # wincmd('mvn clean install -U -T 1C -Dmaven.test.skip=true -Dmaven.compile.fork=true')   # 编译
    ssh = SSH('172.16.101.225', 'root', 'tebon2017')    # 连接服务器
    # ssh.ssh_shell('ls -a')
    ssh.sftp_put('D:/WorkSpace/GitLab/cloud2_new/tebonx-cloud-xrkj-ui/src', '/usr/kjbiz-front/kjbiz-ui-nginx/src')   # 上传文件
    # ssh.ssh_shell('sh /root/war_bak/xrbiz-server/update_war.sh')  # 启动服务
    ssh.sftp_get('/root/war_bak/dist/index.html', 'C:/Users/tebon/Desktop/index.html')  # 下载文件