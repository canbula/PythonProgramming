# sftp_client.py
import wx
from pubsub import pub
from threading import Thread
import paramiko
from stat import S_ISDIR
import os
from datetime import datetime
def send_status(message, topic='update_status'):
    """SFTP işlem durumunu güncellemek için kullanılan fonksiyon."""
    wx.CallAfter(pub.sendMessage, topic, message=message)

class Path:
    """SFTP sunucusundaki dosya veya dizinler için bir yol nesnesi."""
    def __init__(self, ftype, size, filename, date):
        self.folder = S_ISDIR(ftype)
        self.size = size
        self.filename = filename
        self.last_modified = date

class SFTP:
    """SFTP bağlantısını yöneten sınıf."""

    def __init__(self, folder=None):
        self.folder = folder
        self.sftp = None
        self.transport = None

    def connect(self, host, port, username, password):
        """SFTP sunucusuna bağlanır."""
        try:
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username=username, password=password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            welcome_message = "Connected to SFTP server"
            send_status(welcome_message)
            send_status('Connected to server without any errors.', topic='update_statusbar')
            self.get_dir_listing()
        except paramiko.AuthenticationException as e:
            send_status(f'Authentication error: {e}', topic='update_statusbar')
        except Exception as e:
            send_status(f'Disconnected: {str(e)}', topic='update_statusbar')

    def disconnect(self):
        """SFTP sunucusundan bağlantıyı keser."""
        if self.sftp:
            try:
                goodbye_message = "Disconnected from SFTP server"
                send_status(goodbye_message)
                self.sftp.close()
                self.transport.close()
                send_status('Disconnected from server without any errors.', topic='update_statusbar')
            except Exception as e:
                send_status(f'Error during disconnect: {str(e)}', topic='update_statusbar')

    def change_directory(self, folder):
        """Sunucu üzerindeki dizini değiştirir."""
        try:
            self.sftp.chdir(folder)
            self.get_dir_listing()
            current_directory = self.sftp.getcwd()
            send_status(f'Changed directory to {current_directory}')
        except Exception as e:
            send_status(f'Error changing directory: {str(e)}')

    def prev_directory(self):
        """Üst dizine geçiş yapar."""
        if not self.sftp:
            wx.MessageBox("You have to establish a connection first !", "Error", wx.OK | wx.ICON_ERROR)
        else:
            try:
                self.sftp.chdir('..')
                self.get_dir_listing()
                current_directory = self.sftp.getcwd()
                send_status(f'Changed directory to {current_directory}')
            except Exception as e:
                send_status(f'Error changing to previous directory: {str(e)}')
    def get_dir_listing(self):
        """Dizin listesini alır."""
        if self.sftp:
            data = self.sftp.listdir_attr()
            self.parse_data(data)

    def parse_data(self, data):
        """Dizin verilerini analiz eder."""
        paths = []
        for item in data:
            ftype = item.st_mode
            size = int(int(item.st_size)/1024)
            if size == 0:
                size = "0 KB"
            else:
                size = str(size).__add__(" KB")
            filename = item.filename
            date = datetime.fromtimestamp(item.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            if filename == '.':
                continue
            paths.append(Path(ftype, size, filename, date))

        wx.CallAfter(pub.sendMessage, 'update', paths=paths)

    def delete_file(self, filename):
        """Dosyayı siler."""
        try:
            self.sftp.remove(filename)
            send_status(f'{filename} deleted successfully')
            self.get_dir_listing()
        except Exception as e:
            send_status(f'Unable to delete {filename}: {str(e)}')

    def rename(self, from_name, to_name):
        """Sunucudaki dosya veya dizini yeniden adlandırır."""
        try:
            self.sftp.rename(from_name, to_name)
            send_status(f'{from_name} renamed to {to_name}')
            self.get_dir_listing()
        except Exception as e:
            send_status(f'Error renaming {from_name} to {to_name}: {str(e)}')

    def download_file(self, remote_path, local_path):
        """Dosyayı indirir."""
        try:
            self.sftp.get(remote_path, local_path)
            send_status(f"Downloaded {remote_path} successfully.")
            self.get_dir_listing()
        except Exception as e:
            send_status(f"Failed to download {remote_path}: {str(e)}")

    def upload_file(self, local_path, remote_path):
        """Dosyayı sunucuya yükler."""
        try:
            self.sftp.put(local_path, remote_path)
            send_status(f"Uploaded {local_path} successfully.")
            self.get_dir_listing()
        except Exception as e:
            send_status(f"Failed to upload {local_path}: {str(e)}")

    def copy_file(self, src, dst):
        """Sunucuda dosyayı bir konumdan diğerine kopyalar."""
        try:
            temp_file = 'tempfile'
            self.sftp.get(src, temp_file)  # Remote to local
            self.sftp.put(temp_file, dst)  # Local to remote
            os.remove(temp_file)
            send_status(f'File copied from {src} to {dst}')
            self.get_dir_listing()
        except Exception as e:
            send_status(f'Error copying file from {src} to {dst}: {str(e)}')

    def copy_folder(self, src, dst):
        """Sunucuda klasörü bir konumdan diğerine kopyalar."""
        try:
            self._copy_folder_recursive(src, dst)
            send_status(f'Folder copied from {src} to {dst}')
        except Exception as e:
            send_status(f'Error copying folder from {src} to {dst}: {str(e)}')