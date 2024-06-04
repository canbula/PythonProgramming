# ftp_client.py
import os
import wx
from ftplib import FTP as ftplib_FTP, error_perm
from pubsub import pub

def send_status(message, topic='update_status'):
    """Durum güncellemelerini yayınlar."""
    wx.CallAfter(pub.sendMessage, topic, message=message)

class Path:
    """FTP sunucusundaki dosya veya dizinler için bir yol nesnesi."""
    def __init__(self, ftype, size, filename, date):
        self.folder = 'd' in ftype
        self.size = size
        self.filename = filename
        self.last_modified = date
class FTP:
    """FTP bağlantısını yöneten sınıf."""

    def __init__(self, folder=None):
        self.folder = folder
        self.ftp = None

    def connect(self, host, port, username, password):
        """FTP sunucusuna bağlanır."""
        try:
            self.ftp = ftplib_FTP()
            self.ftp.connect(host, port)
            self.ftp.login(username, password)
            welcome_message = "Connected to FTP server"
            send_status(welcome_message)
            send_status('Connected to server wthiout any errors.', topic='update_statusbar')
            self.get_dir_listing()
        except error_perm as e:
            send_status(f'Permission error: {e}', topic='update_statusbar')

        except Exception as e:
            if str(e).startswith('[Errno 11001]'):
                send_status(f'Disconnected: {str(e)}. Please check the hostname or IP address.', topic='update_statusbar')
            else:
                send_status(f'Disconnected: {str(e)}', topic='update_statusbar')


    def disconnect(self):
        """FTP sunucusundan bağlantıyı keser."""
        if self.ftp:
            try:
                goodbye_message = "Disconnected from FTP server"
                send_status(goodbye_message)
                self.ftp.quit()
                send_status('Disconnected from server without any errors.', topic='update_statusbar')
            except Exception as e:
                send_status(f'Error during disconnect: {str(e)}', topic='update_statusbar')

    def change_directory(self, folder):
        """Sunucu üzerindeki dizini değiştirir."""
        try:
            self.ftp.cwd(folder)
            self.get_dir_listing()
            current_directory = self.ftp.pwd()
            send_status(f'Changed directory to {current_directory}')
        except Exception as e:
            send_status(f'Error changing directory: {str(e)}')

    def prev_directory(self):
        try:
            self.ftp.cwd('..')
            self.get_dir_listing()
            current_directory = self.ftp.pwd()
            send_status(f'Changed directory to {current_directory}')
        except Exception as e:
            send_status(f'Error changing to previous directory: {str(e)}')
    def get_dir_listing(self):
        """Dizin listesini alır."""
        if self.ftp:
            data = []
            self.ftp.dir(data.append)
            self.parse_data(data)
        else:
            data = []

    def parse_data(self, data):
        """Dizin verilerini analiz eder."""
        paths = []
        for item in data:
            parts = item.split()
            ftype = parts[0]
            size = int(int(parts[4])/1024)
            if size == 0:
                size = "0 KB"
            else:
                size = str(size).__add__(" KB")
            if len(parts) > 9:
                filename = ' '.join(parts[8:])
            else:
                filename = parts[8]
            date = '{month} {day} {t}'.format(
                month=parts[5], day=parts[6], t=parts[7])
            if filename == '.':
                continue
            paths.append(Path(ftype, size, filename, date))

        wx.CallAfter(pub.sendMessage, 'update', paths=paths)

    def delete_file(self, filename):
        """Dosyayı siler."""
        try:
            self.ftp.delete(filename)
            send_status(f'{filename} deleted successfully')
            self.get_dir_listing()
        except Exception as e:
            send_status(f'Unable to delete {filename}: {str(e)}')

    def rename(self, from_name, to_name):
        """Sunucudaki dosya veya dizini yeniden adlandırır."""
        try:
            self.ftp.rename(from_name, to_name)
            send_status(f'{from_name} renamed to {to_name}')
            self.get_dir_listing()
        except Exception as e:
            send_status(f'Error renaming {from_name} to {to_name}: {str(e)}')

    def download_files(self, paths, local_folder):
        """Dosyaları indirir."""
        for path in paths:
            try:
                full_path = os.path.join(local_folder, os.path.basename(path))
                with open(full_path, 'wb') as local_file:
                    self.ftp.retrbinary(f'RETR {path}', local_file.write)
                    send_status(f'Downloaded: {path}')
            except Exception as e:
                send_status(f'Error downloading {path}: {str(e)}')


    def upload_files(self, local_path, remote_path):
        """Dosyayı FTP sunucusuna yükler."""
        try:
            with open(local_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {remote_path}', file)
            send_status(f"Uploaded {local_path} successfully.")
            self.get_dir_listing()
        except Exception as e:
            send_status(f"Failed to upload {local_path}: {str(e)}")

    def copy_file(self, src, dst):
        """Sunucuda dosyayı bir konumdan diğerine kopyalar."""
        try:
            with open('tempfile', 'wb') as f:
                self.ftp.retrbinary(f'RETR {src}', f.write)
            with open('tempfile', 'rb') as f:
                self.ftp.storbinary(f'STOR {dst}', f)
            os.remove('tempfile')
            send_status(f'File copied from {src} to {dst}')
            self.get_dir_listing()
        except Exception as e:
            send_status(f'Error copying file from {src} to {dst}: {str(e)}')

    def copy_folder(self, src, dst):
        """Sunucuda klasörü bir konumdan diğerine kopyalar."""
        try:
            if not self.path_exists(dst):
                self.ftp.mkd(dst)
            for item in self.ftp.nlst(src):
                item_name = os.path.basename(item)
                src_item = os.path.join(src, item_name)
                dst_item = os.path.join(dst, item_name)
                if self.is_directory(src_item):
                    self.copy_folder(src_item, dst_item)
                else:
                    self.copy_file(src_item, dst_item)
            send_status(f'Folder copied from {src} to {dst}')
        except Exception as e:
            send_status(f'Error copying folder from {src} to {dst}: {str(e)}')
