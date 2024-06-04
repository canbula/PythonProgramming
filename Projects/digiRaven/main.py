# main.py
import wx
from pubsub import pub
import threading
import time
import os
from database import Firebase
from ObjectListView import ObjectListView, ColumnDefn
from ftp_client import FTP
from sftp_client import SFTP


def send_status(message, topic='update_status'):
    wx.CallAfter(pub.sendMessage, topic, message=message)

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, panel):
        wx.FileDropTarget.__init__(self)
        self.panel = panel

    def OnDropFiles(self, x, y, filenames):
        self.panel.upload_files(filenames)
        return True


class FtpPanel(wx.Panel):
    """FTP işlemlerini gösteren panel."""
    def __init__(self, parent):
        super().__init__(parent)
        self.ftp = None
        self.sftp = None
        self.paths = []
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.create_ui()
        self.SetSizer(self.main_sizer)
        pub.subscribe(self.update, 'update')
        pub.subscribe(self.update_status, 'update_status')
        self.SetDropTarget(FileDropTarget(self))

    def list_reset(self):
        self.remote_server.SetEmptyListMsg("Not Connected")
    def create_ui(self):
        """Paneldeki kullanıcı arayüzünü oluşturur."""
        size = (150, -1)
        connect_sizer = wx.BoxSizer()

        host_lbl = wx.StaticText(self, label='Host:')
        connect_sizer.Add(host_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.host = wx.TextCtrl(self, size=size)
        connect_sizer.Add(self.host, 0, wx.ALL, 5)

        user_lbl = wx.StaticText(self, label='Username:')
        connect_sizer.Add(user_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.user = wx.TextCtrl(self, size=size)
        connect_sizer.Add(self.user, 0, wx.ALL, 5)

        password_lbl = wx.StaticText(self, label='Password:')
        connect_sizer.Add(password_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.password = wx.TextCtrl(self, size=size, style=wx.TE_PASSWORD)
        connect_sizer.Add(self.password, 0, wx.ALL, 5)

        port_lbl = wx.StaticText(self, label='Port:')
        connect_sizer.Add(port_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.port = wx.TextCtrl(self, size=(50, -1))
        connect_sizer.Add(self.port, 0, wx.ALL, 5)

        protocol_lbl = wx.StaticText(self, label='Protocol:')
        connect_sizer.Add(protocol_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.protocol_choice = wx.Choice(self, choices=["FTP", "SFTP"])
        connect_sizer.Add(self.protocol_choice, 0, wx.ALL, 5)

        connect_btn = wx.Button(self, label='Connect')
        connect_btn.Bind(wx.EVT_BUTTON, self.on_connect)
        connect_sizer.Add(connect_btn, 0, wx.ALL, 5)

        disconnect_btn = wx.Button(self, label='Disconnect')
        disconnect_btn.Bind(wx.EVT_BUTTON, self.twotime)
        connect_sizer.Add(disconnect_btn, 0, wx.ALL, 5)



        self.main_sizer.Add(connect_sizer)


        self.status = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.main_sizer.Add(self.status, 1, wx.ALL | wx.EXPAND, 5)

        folder_ico = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_TOOLBAR, (16, 16))
        file_ico = wx.ArtProvider.GetBitmap(wx.ART_HELP_PAGE, wx.ART_TOOLBAR, (16, 16))
        self.remote_server = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.remote_server.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_change_directory)
        self.remote_server.AddNamedImages('folder', smallImage=folder_ico)
        self.remote_server.AddNamedImages('file', smallImage=file_ico)
        self.remote_server.SetEmptyListMsg("Not Connected")
        self.main_sizer.Add(self.remote_server, 2, wx.ALL | wx.EXPAND, 5)
        self.update_ui()

    def on_logout(self,event):
        FtpFrame.on_logout(self)

    def twotime(self, event):
        self.on_disconnect(event)
        self.on_disconnect(event)
    def on_connect(self, event):
        host = self.host.GetValue()
        username = self.user.GetValue()
        password = self.password.GetValue()
        try:
            port = int(self.port.GetValue())
        except:
            port = 0
        protocol = self.protocol_choice.GetStringSelection()
        parent_frame = self.GetTopLevelParent()
        status_bar = parent_frame.GetStatusBar()
        status_bar.SetStatusText('Connecting...', 1)

        if host and username and password and port:
            if protocol == "FTP":
                self.ftp = FTP()
                args = [self.ftp, host, port, username, password]
                self.thread = threading.Thread(target=self.connect_thread, args=args)
                self.thread.daemon = True
                self.thread.start()
                self.remote_server.SetEmptyListMsg("Invalid login arguments.")  # Bağlantı sağlandığında boş liste mesajını güncelle


            elif protocol == "SFTP":
                self.sftp = SFTP()
                args = [self.sftp, host, port, username, password]
                self.thread = threading.Thread(target=self.connect_sftp_thread, args=args)
                self.thread.daemon = True
                self.thread.start()
                self.remote_server.SetEmptyListMsg("Invalid login arguments.")  # Bağlantı sağlandığında boş liste mesajını güncelle
            else:
                self.remote_server.SetEmptyListMsg("All required fields must be filled in.")
                status_bar.SetStatusText('Connection failed.', 1)
        elif not protocol == "SFTP" or not protocol == "FTP":
            self.remote_server.SetEmptyListMsg("All required fields must be filled in.")
            status_bar.SetStatusText('Connection failed.', 1)
    def on_disconnect(self, event):
        protocol = self.protocol_choice.GetStringSelection()
        if protocol == "FTP":
            if self.ftp:
                self.ftp.disconnect()
        elif protocol == "SFTP":
            if self.sftp:
                self.sftp.disconnect()

        parent_frame = self.GetTopLevelParent()
        status_bar = parent_frame.GetStatusBar()
        status_bar.SetStatusText('Disconnected', 1)
        self.paths = []
        self.remote_server.SetEmptyListMsg("Not Connected")
        self.update_ui()

        self.protocol_choice.Clear()
        self.protocol_choice.Append("FTP")
        self.protocol_choice.Append("SFTP")

    def connect_thread(self, ftp, host, port, username, password):
        ftp.connect(host, port, username, password)

    def connect_sftp_thread(self, sftp, host, port, username, password):
        sftp.connect(host, port, username, password)

    def change_dir_thread(self, ftp, folder):
        ftp.change_directory(folder)

    def change_dir_sftp_thread(self, sftp, folder):
        sftp.change_directory(folder)

    def rename_thread(self, ftp, old_name, new_name):
        ftp.rename(old_name, new_name)

    def rename_sftp_thread(self, sftp, old_name, new_name):
        sftp.rename(old_name, new_name)

    def prev_directory_thread(self, sftp):
        sftp.prev_directory()

    def copy_file_thread(self, ftp, src, dst):
        ftp.copy_file(src, dst)

    def copy_file_sftp_thread(self, sftp, src, dst):
        sftp.copy_file(src, dst)

    def copy_folder_thread(self, ftp, src, dst):
        ftp.copy_folder(src, dst)

    def copy_folder_sftp_thread(self, sftp, src, dst):
        sftp.copy_folder(src, dst)

    def image_getter(self, path):
        if path.folder:
            return "folder"
        else:
            return "file"

    def on_change_directory(self, event):
        current_selection = self.remote_server.GetSelectedObject()
        if current_selection.folder:
            protocol = self.protocol_choice.GetStringSelection()
            if protocol == "FTP":
                self.thread = threading.Thread(target=self.change_dir_thread, args=[self.ftp, current_selection.filename])
            elif protocol == "SFTP":
                self.thread = threading.Thread(target=self.change_dir_sftp_thread, args=[self.sftp, current_selection.filename])
            self.thread.daemon = True
            self.thread.start()

    def on_copy(self, event):
        selections = self.remote_server.GetSelectedObjects()
        if not selections:
            wx.MessageBox("No file or folder selected for copying", "Error", wx.OK | wx.ICON_ERROR)
            return
        for selection in selections:
            src = selection.filename
            dst = wx.GetTextFromUser(f'Enter the copy name', 'Copy')
            if dst:
                protocol = self.protocol_choice.GetStringSelection()
                if protocol == "FTP":
                    if selection.folder:
                        self.thread = threading.Thread(target=self.copy_folder_thread, args=[self.ftp, src, dst])
                    else:
                        self.thread = threading.Thread(target=self.copy_file_thread, args=[self.ftp, src, dst])
                elif protocol == "SFTP":
                    if selection.folder:
                        self.thread = threading.Thread(target=self.copy_folder_sftp_thread, args=[self.sftp, src, dst])
                    else:
                        self.thread = threading.Thread(target=self.copy_file_sftp_thread, args=[self.sftp, src, dst])
                self.thread.daemon = True
                self.thread.start()
    def on_rename(self, event):
        selection = self.remote_server.GetSelectedObject()
        if not selection:
            wx.MessageBox("No file selected for renaming", "Error", wx.OK | wx.ICON_ERROR)
            return
        new_name = wx.GetTextFromUser(f'Enter new name for {selection.filename}', 'Rename')
        if new_name:
            protocol = self.protocol_choice.GetStringSelection()
            if protocol == "FTP":
                self.thread = threading.Thread(target=self.rename_thread, args=[self.ftp, selection.filename, new_name])
            elif protocol == "SFTP":
                self.thread = threading.Thread(target=self.rename_sftp_thread, args=[self.sftp, selection.filename, new_name])
            self.thread.daemon = True
            self.thread.start()

    def on_prev_directory(self, event):
        protocol = self.protocol_choice.GetStringSelection()
        if protocol == "FTP":
            if self.ftp:
                self.ftp.prev_directory()
        elif protocol == "SFTP":
            if self.sftp:
                self.sftp.prev_directory()
        else:
            wx.MessageBox(f"You have to establish a connection first !", "Error", wx.OK | wx.ICON_ERROR)

    def update(self, paths):
        self.paths = paths
        self.update_ui()

    def update_status(self, message):
        ts = time.strftime('%H:%M:%S', time.localtime())
        if '\n' in message:
            for line in message.split('\n'):
                line = f'{ts} {line}'
                self.status.WriteText(f'{line}\n')
        else:
            message = f'{ts} {message}'
            self.status.WriteText(f'{message}\n')

    def update_ui(self):
        self.remote_server.SetColumns([
            ColumnDefn("File/Folder", "left", 800, "filename", imageGetter=self.image_getter),
            ColumnDefn("Filesize", "right", 80, "size"),
            ColumnDefn("Last Modified", "left", 150, "last_modified")
        ])
        protocol = self.protocol_choice.GetStringSelection()

        self.remote_server.SetObjects(self.paths)
        if not self.paths:
            if protocol:
                self.remote_server.SetEmptyListMsg("No file found")  # Boş liste mesajını ayarla
            else:
                self.remote_server.SetEmptyListMsg("Not Connected")


    def upload_files(self, filenames):
        protocol = self.protocol_choice.GetStringSelection()
        if protocol == "FTP":
            if not self.ftp:
                wx.MessageBox("Not connected to any FTP server.", "Error", wx.OK | wx.ICON_ERROR)
                return
            for file in filenames:
                remote_path = os.path.basename(file)
                self.ftp.upload_files(file, remote_path)
        elif protocol == "SFTP":
            if not self.sftp:
                wx.MessageBox("Not connected to any SFTP server.", "Error", wx.OK | wx.ICON_ERROR)
                return
            for file in filenames:
                remote_path = os.path.basename(file)
                self.sftp.upload_file(file, remote_path)

    def download_files(self, filenames):
        protocol = self.protocol_choice.GetStringSelection()
        if protocol == "FTP":
            if not self.ftp:
                wx.MessageBox("Not connected to any FTP server.", "Error", wx.OK | wx.ICON_ERROR)
                return
            for file in filenames:
                self.ftp.download_files([file], '.')
        elif protocol == "SFTP":
            if not self.sftp:
                wx.MessageBox("Not connected to any SFTP server.", "Error", wx.OK | wx.ICON_ERROR)
                return
            for file in filenames:
                self.sftp.download_file(file, '.')

    def go_home(self):
        protocol = self.protocol_choice.GetStringSelection()
        if protocol == "FTP" and self.ftp:
            self.ftp.change_directory('/')
        elif protocol == "SFTP" and self.sftp:
            self.sftp.change_directory('/')
        else:
            wx.MessageBox(f"You have to establish a connection first !", "Error", wx.OK | wx.ICON_ERROR)





class FtpFrame(wx.Frame):
    def __init__(self, parent, title, user, f: Firebase):
        super(FtpFrame, self).__init__(parent, title=title, size=(1060, 600))
        self.user = user
        self.f = f
        self.panel = FtpPanel(self)
        self.create_toolbar()
        self.is_logging_out = False  # Logout bayrağı
        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusText('Disconnected', 1)
        pub.subscribe(self.update_statusbar, 'update_statusbar')
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Pencere kapatma olayı bağlama
        self.Center()
        self.Show()



    def create_toolbar(self):
        self.toolbar = self.CreateToolBar()
        icon = wx.Icon("icon.png", wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        def resize_icon(icon_path, size=(25, 25)):
            img = wx.Image(icon_path, wx.BITMAP_TYPE_ANY)
            img = img.Scale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
            return wx.Bitmap(img)

        self.toolbar.AddSeparator()
        home_ico = resize_icon("home.ico")
        home_tool = self.toolbar.AddTool(wx.ID_ANY, 'Go to root directory', home_ico, 'Go to root directory')
        self.Bind(wx.EVT_TOOL, self.on_home_button, home_tool)
        self.toolbar.AddSeparator()

        upload_ico = resize_icon("upload.ico")
        upload_tool = self.toolbar.AddTool(wx.ID_ANY, 'Upload File', upload_ico, 'Upload a file')
        self.Bind(wx.EVT_TOOL, self.on_upload_file, upload_tool)
        self.toolbar.AddSeparator()

        add_ico = resize_icon("download.ico")
        add_file_tool = self.toolbar.AddTool(wx.ID_ANY, 'Download File', add_ico, 'Download a file')
        self.Bind(wx.EVT_TOOL, self.on_download_file, add_file_tool)
        self.toolbar.AddSeparator()


        remove_ico = resize_icon("delete.ico")
        remove_tool = self.toolbar.AddTool(wx.ID_ANY, 'Remove File', remove_ico, 'Remove file')
        self.Bind(wx.EVT_TOOL, self.on_remove, remove_tool)
        self.toolbar.AddSeparator()

        rename_ico = resize_icon("rename.ico")
        rename_tool = self.toolbar.AddTool(wx.ID_ANY, 'Rename', rename_ico, 'Rename file or folder')
        self.Bind(wx.EVT_TOOL, self.panel.on_rename, rename_tool)
        self.toolbar.AddSeparator()

        copy_ico = resize_icon("duplicate_transparent.ico")
        copy_tool = self.toolbar.AddTool(wx.ID_ANY, 'Copy', copy_ico, 'Copy file or folder')
        self.Bind(wx.EVT_TOOL, self.panel.on_copy, copy_tool)
        self.toolbar.AddSeparator()

        getback_ico = resize_icon("prev.ico")
        getback_tool = self.toolbar.AddTool(wx.ID_ANY, 'Go back to previous directory', getback_ico, 'Go back to previous directory')
        self.Bind(wx.EVT_TOOL, self.panel.on_prev_directory, getback_tool)
        for i in range(90):
            self.toolbar.AddSeparator()



        self.toolbar.Realize()


    def on_close(self, event):
        if not self.is_logging_out:
            self.Destroy()  # Pencereyi kapat
        else:
            self.Destroy()  # Pencereyi kapat
            wx.CallAfter(login_check, self.f)  # Login ekranına geri dön
    def on_upload_file(self, event):
        protocol = self.panel.protocol_choice.GetStringSelection()
        if protocol == "":
            wx.MessageBox("Not connected to any server.", "Error", wx.OK | wx.ICON_ERROR)
            return
        with wx.FileDialog(self, "Choose a file to upload", wildcard="*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                if protocol == "FTP":
                    self.panel.ftp.upload_files(pathname, os.path.basename(pathname))
                elif protocol == "SFTP":
                    self.panel.sftp.upload_file(pathname, os.path.basename(pathname))
                wx.MessageBox(f"File {pathname} uploaded successfully", "Info", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error uploading file: {e}", "Error", wx.OK | wx.ICON_ERROR)


    def on_download_file(self, event):
        protocol = self.panel.protocol_choice.GetStringSelection()
        if protocol == "":
            wx.MessageBox("Not connected to any server.", "Error", wx.OK | wx.ICON_ERROR)
            return
        selections = self.panel.remote_server.GetSelectedObjects()
        if not selections:
            wx.MessageBox("No file selected for download", "Error", wx.OK | wx.ICON_ERROR)
            return
        with wx.DirDialog(self, "Choose a directory to save downloaded file", style=wx.DD_DEFAULT_STYLE) as dirDialog:
            if dirDialog.ShowModal() == wx.ID_CANCEL:
                return
            download_path = dirDialog.GetPath()
            for selection in selections:
                remote_file_path = selection.filename
                local_file_path = os.path.join(download_path, os.path.basename(remote_file_path))
                try:
                    #protocol = self.panel.protocol_choice.GetStringSelection()
                    if protocol == "FTP":
                        self.panel.ftp.download_files([remote_file_path], download_path)
                    elif protocol == "SFTP":
                        self.panel.sftp.download_file(remote_file_path, local_file_path)
                    wx.MessageBox(f"File {remote_file_path} downloaded successfully to {download_path}", "Info",
                                  wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"Error downloading file: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_remove(self, event):
        selection = self.panel.remote_server.GetSelectedObject()
        if not selection:
            wx.MessageBox("No file selected for deletion", "Error", wx.OK | wx.ICON_ERROR)
            return
        with wx.MessageDialog(parent=None, message=f'Do you really want to delete {selection.filename}?',
                              caption='Confirmation', style=wx.OK | wx.CANCEL | wx.ICON_QUESTION) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    protocol = self.panel.protocol_choice.GetStringSelection()
                    if protocol == "FTP":
                        self.panel.ftp.delete_file(selection.filename)
                    elif protocol == "SFTP":
                        self.panel.sftp.delete_file(selection.filename)
                    wx.MessageBox(f"File {selection.filename} deleted successfully", "Info", wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"Error deleting file: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_home_button(self, event):
        self.panel.go_home()
    def update_statusbar(self, message):
        self.statusbar.SetStatusText(message, 1)


class Dialog(wx.Frame):
    """FTP istemcisini gösteren pencere sınıfı."""

    def __init__(self, parent, title, f:Firebase):
        super(Dialog, self).__init__(parent, title=title, size=(1024, 768),
                                     style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.f = f
        self.closed = False
        self.user = None
        self.init_ui()
        self.Centre()
        self.Show()

    def init_ui(self):
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        icon = wx.Icon("icon.png", wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        # Sol tarafta fotoğraf için panel
        left_panel = wx.Panel(panel)
        left_panel.SetBackgroundColour(wx.WHITE)
        vbox_left = wx.BoxSizer(wx.VERTICAL)

        # Fotoğraf ekleme
        bitmap = wx.Bitmap("digi.png", wx.BITMAP_TYPE_ANY)
        bitmap = scale_bitmap(bitmap, 580, 580)
        logo = wx.StaticBitmap(left_panel, bitmap=bitmap)
        vbox_left.Add(logo, 1, wx.EXPAND | wx.ALL,0)
        left_panel.SetSizer(vbox_left)

        # Sağ tarafta giriş alanları ve butonlar için panel
        right_panel = wx.Panel(panel)
        right_panel.SetBackgroundColour(wx.LIGHT_GREY)
        vbox_right = wx.BoxSizer(wx.VERTICAL)

        font1 = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Cascadia Code")

        email_label = wx.StaticText(right_panel, label="Email:", style=wx.ALIGN_CENTER, size=(100, 20))
        email_label.SetFont(font1)
        vbox_right.Add(email_label, 0, wx.ALIGN_CENTER | wx.TOP, 150)

        self.email_entry = wx.TextCtrl(right_panel, style=wx.TE_CENTER,
                                       size=(200, 20))
        vbox_right.Add(self.email_entry, 0, wx.EXPAND | wx.ALL, 10)

        password_label = wx.StaticText(right_panel, label="Password:", style=wx.ALIGN_CENTER, size=(100, 20))
        password_label.SetFont(font1)
        vbox_right.Add(password_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        self.password_entry = wx.TextCtrl(right_panel, style=wx.TE_PASSWORD | wx.TE_CENTER,
                                          size=(200, 20))
        vbox_right.Add(self.password_entry, 0, wx.EXPAND | wx.ALL, 10)

        button_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial")

        # login_button = wx.Button(right_panel, label="Login")
        login_button = wx.Button(right_panel, label="Login", size=(100, 30))
        login_button.SetFont(button_font)
        login_button.SetBackgroundColour(wx.Colour(0, 128, 255))  # Arka plan rengi
        login_button.SetForegroundColour(wx.WHITE)  # Yazı rengi
        login_button.Bind(wx.EVT_BUTTON, self.on_login)
        vbox_right.Add(login_button, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        register_button = wx.Button(right_panel, label="Register", size=(100, 30))
        register_button.SetFont(button_font)
        register_button.SetBackgroundColour(wx.Colour(2, 67, 125))  # Arka plan rengi
        register_button.SetForegroundColour(wx.WHITE)  # Yazı rengi
        # register_button = wx.Button(right_panel, label="Register")
        register_button.Bind(wx.EVT_BUTTON, self.on_register)
        vbox_right.Add(register_button, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        font2 = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial")

        self.error_label = wx.StaticText(right_panel, pos=(20, 100))
        self.error_label.SetForegroundColour(wx.RED)
        self.error_label.SetFont(font2)
        vbox_right.Add(self.error_label, 100, wx.ALIGN_LEFT | wx.TOP, 10)

        right_panel.SetSizer(vbox_right)

        # Panelleri ana sizer'a ekleme
        hbox.Add(left_panel, 3, wx.EXPAND | wx.ALL, 0)
        hbox.Add(right_panel, 1, wx.EXPAND | wx.ALL, 0)

        panel.SetSizer(hbox)


        self.SetSize((800, 600))
        self.Centre()

    def on_login(self, event):
        email = self.email_entry.GetValue()
        password = self.password_entry.GetValue()

        try:
            self.user = self.f.login(email, password)
            self.Close()
        except Exception as e:
            print(e)
            self.error_label.SetForegroundColour(wx.Colour(230, 20, 50))
            self.error_label.SetLabel("   * Invalid username or password")

    def on_register(self, event):
        email = self.email_entry.GetValue()
        password = self.password_entry.GetValue()

        if email == "" or password == "":
            self.error_label.SetForegroundColour(wx.Colour(230, 20, 50))
            self.error_label.SetLabel("   * Required fields cannot be left empty.")
        else:
            try:
                self.f.register(email, password)
                self.error_label.SetForegroundColour(wx.Colour(0, 128, 50))
                self.error_label.SetLabel("    Registration successful.\n    You can now log in.")
            except Exception as e:
                self.error_label.SetForegroundColour(wx.Colour(230, 20, 50))

                if len(password) < 6:
                    self.error_label.SetLabel("   * Registration failed.\n   *Password should be at least\n    6 characters")
                elif not self.check_email_format(email):
                    self.error_label.SetLabel("   * Registration failed.\n   * Invalid email format.")
                else:
                    self.error_label.SetLabel("   * Registration failed.\n   * This user is already registered.")
                print(e)

            # self.Close()

    def on_close(self, event):
        self.Destroy()

    def check_email_format(self,email):
        # "@" işaretinin bir kez bulunup bulunmadığını kontrol et
        if email.count("@") != 1:
            return False

        # En az bir adet nokta olup olmadığını kontrol et
        if "." not in email:
            return False

        # "@" işaretinin noktadan önce olup olmadığını kontrol et
        at_index = email.index("@")
        dot_index = email.rindex(".")

        if at_index > dot_index:
            return False

        # "@" ile nokta arasında en az bir karakter olup olmadığını kontrol et
        if dot_index - at_index <= 1:
            return False

        # Nokta ile bitmemesi ve noktadan sonra en az bir karakter gelmesi gerektiğini kontrol et
        if dot_index == len(email) - 1:
            return False

        # Email adresinin son iki karakterinin a-z arası bir karakter olması gerektiğini kontrol et
        if not email[-2:].isalpha() or not email[-2:].islower():
            return False

        return True

        return True

def scale_bitmap(bitmap, width, height):
    """
    Scale the bitmap by the given width and height.
    :param bitmap:
    :param width:
    :param height:
    :return:
    """
    image = bitmap.ConvertToImage()
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    return result



if __name__ == '__main__':
    app = wx.App()
    f = Firebase()

    login_frame = Dialog(None, title="DigiRaven", f=f)
    app.MainLoop()
    if login_frame.user:
        main_frame = FtpFrame(None, title="DigiRaven", user=login_frame.user, f=f)
        app.MainLoop()



