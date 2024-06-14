
from os import getcwd
import paramiko
class Connection:
    global ssh
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    @staticmethod
    def remote_connect(ip,username,password):
        global ftp
        try:
            ssh.connect(ip,port=22,username=username,password=password)

            ftp=ssh.open_sftp()
            return "Connection Successfull!"
        except paramiko.ssh_exception.AuthenticationException:
            return "Authentication failed check your username and password and try again later"
        except TimeoutError:
            return "Connection is unreachable"
        except Exception:
            return "Something went Wrong!"

    @staticmethod
    def list_dir():
        try:
            files=ftp.listdir()
            return files
        except Exception:
            return "Error Occured"
    @staticmethod
    def change(directory):
        try:
            files=ftp.chdir(directory)
            return "Directory changed Successfully!"
        except Exception:
            return "Unsuccessfull!"

    @staticmethod
    def get_file(filename):
        if ftp.getcwd()==None:
            return False
        else:
            try:
                remote_path=ftp.getcwd()+'/'+filename
                local_path=getcwd()+'/'+filename
                ftp.get(remote_path,local_path)
                return True
            except Exception:
                return False
    @staticmethod
    def put_file(filename):
        remote_path=ftp.getcwd()+'/'+filename
        local_path=getcwd()+'/'+filename
        ftp.put(local_path,remote_path)
        return True
    @staticmethod
    def close():
        ftp.close()
        ssh.close()





#d=Connection()
#print(d.remote_connect("192.168.243.204","raja","Raja@123"))
#print(d.get_file("levi.mp4"))
#d.close()
'''
files=d.list_dir()
for i in files:
    print(i)
d.change("Downloads")
files=d.list_dir()
for i in files:
    print(i)
d.get_file("levi.mp4")
d.close()
'''