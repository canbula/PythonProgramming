import paramiko
from datetime import datetime
from stat import S_ISDIR

class SFTPOperations:

    def __init__(self, hostname, port, username, password):
        print(hostname, port, username, password)
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print("Connecting to SFTP server...")
            # Connect to the SSH server
            client.connect(self.hostname, self.port, self.username, self.password)
            print("Connected to SFTP server successfully!")
            # Create an SFTP client
            self.sftp = client.open_sftp()
            print("SFTP session opened.")
        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")
        except paramiko.SSHException as e:
            print("Unable to establish SSH connection:", str(e))
        except paramiko.SFTPException as e:
            print("Unable to establish SFTP connection:", str(e))

    def open_folder(self, path):
        if path == "":
            dosya_listesi = self.sftp.listdir()
        else:
            self.sftp.chdir(path)
            dosya_listesi = self.sftp.listdir(path)

        dosya_dict_listesi = []
        for j, filename in enumerate(dosya_listesi):
            file_attr = self.sftp.stat(filename)
            size = file_attr.st_size
            date = file_attr.st_mtime
            date = datetime.fromtimestamp(date).strftime('%d %b %Y %H:%M')
            dosya_dict = {"Sira": j, "FileName": filename, "TimeStamp": date, "Size": str(size) + " Byte"}
            dosya_dict_listesi.append(dosya_dict)
        return dosya_dict_listesi

    def dosya_yukle(self, remote_path, local_path):
        try:
            # Upload a file to the remote server
            self.sftp.put(local_path, remote_path)
            print("File uploaded successfully!")
        except Exception as e:
            print("Failed to upload file:", str(e))

    def dosya_indir(self, remote_path, local_path):
        try:
            # Download a file from the remote server
            self.sftp.get(remote_path, local_path)
            print("File downloaded successfully!")
        except Exception as e:
            print("Failed to download file:", str(e))

    def edit_file(sftp, remote_path, new_content):
        try:
            # Read the existing file content
            with sftp.open(remote_path, "r") as file:
                content = file.read()

            # Modify the file content
            content += "\n" + new_content

            # Write the modified content back to the file
            with sftp.open(remote_path, "w") as file:
                file.write(content)

            print("File edited successfully!")
        except Exception as e:
            print("Failed to edit file:", str(e))

    def dosya_sil(self, remote_path):
        try:
            # Delete a file from the remote server
            self.sftp.remove(remote_path)
            print("File deleted successfully!")
        except Exception as e:
            print("Failed to delete file:", str(e))
    
    def get_file_details(self, filepath):
        details = {}
        try:
            file_stat = self.sftp.stat(filepath)
            details['FileName'] = filepath.split('/')[-1]
            details['FilePath'] = filepath
            details['Type'] = 'Directory' if S_ISDIR(file_stat.st_mode) else 'File'
            details['Size'] = file_stat.st_size
            details['Change'] = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            details['filemod'] = oct(file_stat.st_mode)[-3:]
            print("File details retrieved successfully!")
        except FileNotFoundError:
            details['Error'] = "File not found"
        return details
    
    def change_file_mode(self,dosyaadi,mod):
        self.sftp.chmod(dosyaadi,int(mod,8))
        print("File permissions changed successfully!")
    def close(self):
        if self.sftp is not None:
            self.sftp.close()
            print("SFTP connection closed.")

# Host = "eu-central-1.sftpcloud.io",  
# Port = 22,
# Username = "e4242123a37e427494b9a57d839b3247",
# Password = "l8G5YEIKUJhdR6nRj4CdKFH3G0hsJF9R",
# deneme="https://sftpcloud.io/tools/free-sftp-server"

#sftp = SFTPOperations("test.rebex.net", 22, "demo", "password")
#if __name__ == "__main__":
#    print(sftp.open_folder("/pub"))