import paramiko

def sftp_connection(func):
    def wrapper(hostname, username, password, *args, **kwargs):
        try:
            # create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=username, password=password)

            # create SFTP client
            sftp = ssh.open_sftp() 

            result = func(sftp, *args, **kwargs)


            sftp.close()
            ssh.close()

            return result

        except Exception as e:
            print("Error while uploading file:", e)    

    return wrapper

@sftp_connection
def sftp_upload(sftp, local_file, remote_file):
    sftp.put(local_file, remote_file)

@sftp_connection
def sftp_download(sftp, remote_file, local_file):
    sftp.get(remote_file, local_file)

@sftp_connection
def sftp_remove(sftp, remote_file):
    sftp.remove(remote_file)

@sftp_connection
def sftp_listdir(sftp, remote_path):
    return sftp.listdir(remote_path)


def getFiles():
    hostname = ''
    username = ''
    password = ''

    remote_path = ''

    remote_files_and_dirs = sftp_listdir(hostname, username, password, remote_path)
    return remote_files_and_dirs
