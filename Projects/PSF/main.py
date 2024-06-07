import wx
import threading
from ftplib import FTP, error_perm
import os
import json
import datetime
import paramiko


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        for filepath in filenames:
            threading.Thread(target=self.window.upload_file, args=(filepath,)).start()
        return True

class FtpDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(FtpDialog, self).__init__(parent, title=title, size=(350, 350))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        st1 = wx.StaticText(panel, label='Server:')
        self.server = wx.TextCtrl(panel)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        hbox1.Add(self.server, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st2 = wx.StaticText(panel, label='Port:')
        self.port = wx.TextCtrl(panel, value="21")
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(st2, flag=wx.RIGHT, border=8)
        hbox2.Add(self.port, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st3 = wx.StaticText(panel, label='Username:')
        self.username = wx.TextCtrl(panel)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(st3, flag=wx.RIGHT, border=8)
        hbox3.Add(self.username, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st4 = wx.StaticText(panel, label='Password:')
        self.password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(st4, flag=wx.RIGHT, border=8)
        hbox4.Add(self.password, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.anonymous_login = wx.CheckBox(panel, label='Anonymous Login')
        self.save_password = wx.CheckBox(panel, label='Save Password', style=wx.CHK_CHECKED)
        vbox.Add(self.anonymous_login, flag=wx.LEFT, border=10)
        vbox.Add(self.save_password, flag=wx.LEFT, border=10)

        st5 = wx.StaticText(panel, label='Previous Connections:')
        vbox.Add(st5, flag=wx.LEFT | wx.TOP, border=10)

        self.server_list = wx.ListBox(panel)
        vbox.Add(self.server_list, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)

        self.load_previous_connections()

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Connect', id=wx.ID_OK)
        btn2 = wx.Button(panel, label='Cancel', id=wx.ID_CANCEL)
        hbox5.Add(btn1)
        hbox5.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def load_previous_connections(self):
        previous_connections = load_ftp_server_info()
        unique_connections = []
        seen = set()
        for connection in previous_connections:
            conn_tuple = (connection['host'], connection['port'], connection['username'])
            if conn_tuple not in seen:
                unique_connections.append(connection)
                seen.add(conn_tuple)

        unique_connections = sorted(unique_connections, key=lambda x: x['timestamp'], reverse=True)

        for connection in unique_connections:
            display_text = f"{connection['host']}:{connection['port']} - {connection['username']}"
            self.server_list.Append(display_text, connection)

        self.server_list.Bind(wx.EVT_LISTBOX, self.on_select_connection)

    def on_select_connection(self, event):
        selection = self.server_list.GetClientData(event.GetSelection())
        self.server.SetValue(selection['host'])
        self.port.SetValue(str(selection['port']))
        self.username.SetValue(selection['username'])
        self.password.SetValue(selection['password'])
        self.anonymous_login.SetValue(False)


class SftpDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(SftpDialog, self).__init__(parent, title=title, size=(350, 350))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        st1 = wx.StaticText(panel, label='Server:')
        self.server = wx.TextCtrl(panel)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        hbox1.Add(self.server, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st2 = wx.StaticText(panel, label='Port:')
        self.port = wx.TextCtrl(panel, value="22")
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(st2, flag=wx.RIGHT, border=8)
        hbox2.Add(self.port, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st3 = wx.StaticText(panel, label='Username:')
        self.username = wx.TextCtrl(panel)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(st3, flag=wx.RIGHT, border=8)
        hbox3.Add(self.username, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st4 = wx.StaticText(panel, label='Password:')
        self.password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(st4, flag=wx.RIGHT, border=8)
        hbox4.Add(self.password, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.save_password = wx.CheckBox(panel, label='Save Password', style=wx.CHK_CHECKED)
        vbox.Add(self.save_password, flag=wx.LEFT, border=10)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Connect', id=wx.ID_OK)
        btn2 = wx.Button(panel, label='Cancel', id=wx.ID_CANCEL)
        hbox5.Add(btn1)
        hbox5.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)


class InfoDialog(wx.Dialog):
    def __init__(self, parent, title, permissions):
        super(InfoDialog, self).__init__(parent, title=title, size=(300, 200))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        st1 = wx.StaticText(panel, label='Permissions:')
        vbox.Add(st1, flag=wx.ALL, border=10)

        self.read_cb = wx.CheckBox(panel, label='Read')
        self.write_cb = wx.CheckBox(panel, label='Write')
        self.execute_cb = wx.CheckBox(panel, label='Execute')

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.read_cb, flag=wx.RIGHT, border=8)
        hbox1.Add(self.write_cb, flag=wx.RIGHT, border=8)
        hbox1.Add(self.execute_cb, flag=wx.RIGHT, border=8)
        vbox.Add(hbox1, flag=wx.ALL, border=10)

        # Set the initial state of the checkboxes based on the permissions
        self.read_cb.SetValue(permissions['read'])
        self.write_cb.SetValue(permissions['write'])
        self.execute_cb.SetValue(permissions['execute'])

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Save', id=wx.ID_OK)
        btn2 = wx.Button(panel, label='Cancel', id=wx.ID_CANCEL)
        hbox2.Add(btn1)
        hbox2.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.on_save, btn1)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, btn2)

        self.permissions = permissions

    def on_save(self, event):
        self.permissions['read'] = self.read_cb.GetValue()
        self.permissions['write'] = self.write_cb.GetValue()
        self.permissions['execute'] = self.execute_cb.GetValue()
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)


class HistoryDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(HistoryDialog, self).__init__(parent, title=title, size=(400, 300))

        self.parent = parent  # Parent frame reference
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.history_list = wx.ListBox(panel)
        vbox.Add(self.history_list, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)

        self.load_history()

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        delete_btn = wx.Button(panel, label='Delete', id=wx.ID_DELETE)
        close_btn = wx.Button(panel, label='Close', id=wx.ID_CLOSE)
        hbox.AddStretchSpacer()
        hbox.Add(delete_btn, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        hbox.Add(close_btn, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        hbox.AddStretchSpacer()

        vbox.Add(hbox, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.on_close, close_btn)
        self.Bind(wx.EVT_BUTTON, self.on_delete, delete_btn)  # Bind delete button
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_select_connection, self.history_list)  # Bind double-click event

    def load_history(self):
        previous_connections = load_ftp_server_info()
        unique_connections = []
        seen = set()
        for connection in previous_connections:
            conn_tuple = (connection['host'], connection['port'], connection['username'])
            if conn_tuple not in seen:
                unique_connections.append(connection)
                seen.add(conn_tuple)

        unique_connections = sorted(unique_connections, key=lambda x: x['timestamp'], reverse=True)

        for connection in unique_connections:
            display_text = f"{connection['host']}:{connection['port']} - {connection['username']} - {connection.get('timestamp', 'No timestamp')}"
            self.history_list.Append(display_text, connection)

    def on_select_connection(self, event):
        selection = self.history_list.GetClientData(event.GetSelection())
        self.parent.connect_ftp(
            selection['host'],
            selection['port'],
            selection['username'],
            selection['password'],  # Use saved password
            False,  # Assume not anonymous for history connections
            False  # Save password is not relevant here
        )
        self.Destroy()

    def on_delete(self, event):
        selection = self.history_list.GetSelection()
        if selection != wx.NOT_FOUND:
            connection = self.history_list.GetClientData(selection)
            self.history_list.Delete(selection)
            remove_server_info(connection)

    def on_close(self, event):
        self.Destroy()


def remove_server_info(server_info):
    file_path = "ftp_server_info.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        data = [item for item in data if (item['host'], item['port'], item['username']) != (server_info['host'], server_info['port'], server_info['username'])]
        with open(file_path, "w") as file:
            json.dump(data, file)


def remove_bookmark_info(bookmark_info):
    file_path = "bookmarks_info.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        data = [item for item in data if (item['host'], item['port'], item['username']) != (bookmark_info['host'], bookmark_info['port'], bookmark_info['username'])]
        with open(file_path, "w") as file:
            json.dump(data, file)


class BookmarksDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(BookmarksDialog, self).__init__(parent, title=title, size=(400, 300))

        self.parent = parent  # Parent frame reference
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.bookmarks_list = wx.ListBox(panel)
        vbox.Add(self.bookmarks_list, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)

        self.load_bookmarks()

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = wx.Button(panel, label='Add Bookmark')
        delete_btn = wx.Button(panel, label='Delete')
        close_btn = wx.Button(panel, label='Close', id=wx.ID_CLOSE)
        hbox.AddStretchSpacer()
        hbox.Add(add_btn, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        hbox.Add(delete_btn, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        hbox.Add(close_btn, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        hbox.AddStretchSpacer()

        vbox.Add(hbox, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.on_add, add_btn)  # Bind add button
        self.Bind(wx.EVT_BUTTON, self.on_close, close_btn)
        self.Bind(wx.EVT_BUTTON, self.on_delete, delete_btn)  # Bind delete button
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_select_bookmark, self.bookmarks_list)  # Bind double-click event

    def load_bookmarks(self):
        previous_bookmarks = load_bookmark_info()
        unique_bookmarks = []
        seen = set()
        for bookmark in previous_bookmarks:
            conn_tuple = (bookmark['host'], bookmark['port'], bookmark['username'])
            if conn_tuple not in seen:
                unique_bookmarks.append(bookmark)
                seen.add(conn_tuple)

        unique_bookmarks = sorted(unique_bookmarks, key=lambda x: x['timestamp'], reverse=True)

        for bookmark in unique_bookmarks:
            display_text = f"{bookmark['host']}:{bookmark['port']} - {bookmark['username']}"
            self.bookmarks_list.Append(display_text, bookmark)

    def on_add(self, event):
        dlg = FtpDialog(self, 'Add Bookmark')
        if dlg.ShowModal() == wx.ID_OK:
            server = dlg.server.GetValue()
            port = dlg.port.GetValue()
            username = dlg.username.GetValue()
            password = dlg.password.GetValue()
            anonymous_login = dlg.anonymous_login.GetValue()
            save_password = dlg.save_password.GetValue()

            bookmark_info = {
                'host': server,
                'port': port,
                'username': username,
                'password': password if save_password else '',
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            save_bookmark_info(bookmark_info)
            self.load_bookmarks()  # Reload bookmarks to include the new one

        dlg.Destroy()

    def on_select_bookmark(self, event):
        selection = self.bookmarks_list.GetClientData(event.GetSelection())
        self.parent.connect_ftp(
            selection['host'],
            selection['port'],
            selection['username'],
            selection['password'],  # Use saved password
            False,  # Assume not anonymous for bookmarks
            False  # Save password is not relevant here
        )
        self.Destroy()

    def on_delete(self, event):
        selection = self.bookmarks_list.GetSelection()
        if selection != wx.NOT_FOUND:
            bookmark = self.bookmarks_list.GetClientData(selection)
            self.bookmarks_list.Delete(selection)
            remove_bookmark_info(bookmark)

    def on_close(self, event):
        self.Destroy()


class FTPClientFrame(wx.Frame):
    def __init__(self, parent, title):
        super(FTPClientFrame, self).__init__(parent, title=title, size=(1026, 748))
        self.ftp = None
        self.sftp = None  # SFTP bağlantısı için ekleme
        self.current_path = "/"
        self.cached_files = {}
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.create_menu_bar()
        self.create_toolbar(panel)
        self.create_file_list(panel, vbox)

        panel.SetSizerAndFit(vbox)

        self.CreateStatusBar()  # Create the status bar
        self.SetStatusText("No items in file list")  # Set initial status text

        self.Bind(wx.EVT_SIZE, self.on_size)  # Bind the resize event

        icon = wx.Icon(os.path.join(os.getcwd(), 'icons', 'mylogo2.png'), wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        self.Centre()
        self.Show()

    def create_menu_bar(self):
        menubar = wx.MenuBar()

        file_menu = wx.Menu()
        open_item = file_menu.Append(wx.ID_OPEN, '&Open Connection\tCtrl+O')
        disconnect_item = file_menu.Append(wx.ID_EXIT, '&Disconnect\tCtrl+D')
        new_browser_item = file_menu.Append(wx.ID_NEW, '&New Browser\tCtrl+N')
        menubar.Append(file_menu, '&File')

        edit_menu = wx.Menu()
        cut_item = edit_menu.Append(wx.ID_CUT, 'Cu&t\tCtrl+X')
        copy_item = edit_menu.Append(wx.ID_COPY, '&Copy\tCtrl+C')
        paste_item = edit_menu.Append(wx.ID_PASTE, '&Paste\tCtrl+V')
        menubar.Append(edit_menu, '&Edit')

        view_menu = wx.Menu()
        refresh_item = view_menu.Append(wx.ID_REFRESH, '&Refresh\tCtrl+R')
        menubar.Append(view_menu, '&View')

        go_menu = wx.Menu()
        back_item = go_menu.Append(wx.ID_ANY, '&Back')
        forward_item = go_menu.Append(wx.ID_ANY, '&Forward')
        up_item = go_menu.Append(wx.ID_ANY, '&Up')
        menubar.Append(go_menu, '&Go')

        bookmark_menu = wx.Menu()
        add_bookmark_item = bookmark_menu.Append(wx.ID_ANY, '&Add Bookmark')
        manage_bookmarks_item = bookmark_menu.Append(wx.ID_ANY, '&Manage Bookmarks')
        menubar.Append(bookmark_menu, '&Bookmark')

        window_menu = wx.Menu()
        new_window_item = window_menu.Append(wx.ID_ANY, '&New Window')
        close_window_item = window_menu.Append(wx.ID_ANY, '&Close Window')
        menubar.Append(window_menu, '&Window')

        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, '&About')
        menubar.Append(help_menu, '&Help')

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.on_open_connection, open_item)
        self.Bind(wx.EVT_MENU, self.on_disconnect, disconnect_item)
        self.Bind(wx.EVT_MENU, self.on_refresh, refresh_item)
        self.Bind(wx.EVT_MENU, self.on_new_browser, new_browser_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        self.Bind(wx.EVT_MENU, self.on_back, back_item)
        self.Bind(wx.EVT_MENU, self.on_forward, forward_item)
        self.Bind(wx.EVT_MENU, self.on_up, up_item)
        self.Bind(wx.EVT_MENU, self.on_add_bookmark, add_bookmark_item)
        self.Bind(wx.EVT_MENU, self.on_manage_bookmarks, manage_bookmarks_item)
        self.Bind(wx.EVT_MENU, self.on_new_window, new_window_item)
        self.Bind(wx.EVT_MENU, self.on_close_window, close_window_item)
        self.Bind(wx.EVT_MENU, self.on_cut, cut_item)
        self.Bind(wx.EVT_MENU, self.on_copy, copy_item)
        self.Bind(wx.EVT_MENU, self.on_paste, paste_item)

    def create_toolbar(self, panel):
        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        toolbar.SetToolBitmapSize((64, 64))

        # Path to the icons
        logo_icon_path = os.path.join(os.getcwd(), 'icons', 'mylogo2.png')
        refresh_icon_path = os.path.join(os.getcwd(), 'icons', 'refresh.png')
        upload_icon_path = os.path.join(os.getcwd(), 'icons', 'upload.png')
        download_icon_path = os.path.join(os.getcwd(), 'icons', 'download.png')
        delete_icon_path = os.path.join(os.getcwd(), 'icons', 'delete.png')
        disconnect_icon_path = os.path.join(os.getcwd(), 'icons', 'disconnect.png')
        history_icon_path = os.path.join(os.getcwd(), 'icons', 'history.png')  # History icon path
        bookmark_icon_path = os.path.join(os.getcwd(), 'icons', 'bookmark.png')  # Bookmark icon path
        drive_icon_path = os.path.join(os.getcwd(), 'icons', 'drive.png')  # Drive icon path
        sftp_icon_path = os.path.join(os.getcwd(), 'icons', 'sftp.png')  # SFTP icon path
        ftp_icon_path = os.path.join(os.getcwd(), 'icons', 'ftp.png')  # FTP icon path

        logo_tool = toolbar.AddTool(wx.ID_ANY, 'PSF', wx.Bitmap(logo_icon_path))
        toolbar.AddStretchableSpace()  # Add stretchable space to the left
        drive_tool = toolbar.AddTool(wx.ID_ANY, 'Drive', wx.Bitmap(drive_icon_path))  # Add Drive icon
        sftp_tool = toolbar.AddTool(wx.ID_ANY, 'SFTP', wx.Bitmap(sftp_icon_path))  # Add SFTP icon
        ftp_tool = toolbar.AddTool(wx.ID_ANY, 'FTP', wx.Bitmap(ftp_icon_path))  # Add FTP icon
        toolbar.AddSeparator()
        refresh_tool = toolbar.AddTool(wx.ID_REFRESH, 'Refresh', wx.Bitmap(refresh_icon_path))
        toolbar.AddSeparator()
        upload_tool = toolbar.AddTool(wx.ID_ANY, 'Upload', wx.Bitmap(upload_icon_path))
        toolbar.AddSeparator()
        download_tool = toolbar.AddTool(wx.ID_ANY, 'Download', wx.Bitmap(download_icon_path))
        toolbar.AddSeparator()
        delete_tool = toolbar.AddTool(wx.ID_DELETE, 'Delete', wx.Bitmap(delete_icon_path))
        toolbar.AddSeparator()
        history_tool = toolbar.AddTool(wx.ID_ANY, 'History', wx.Bitmap(history_icon_path))  # History tool
        toolbar.AddSeparator()
        bookmark_tool = toolbar.AddTool(wx.ID_ANY, 'Bookmarks', wx.Bitmap(bookmark_icon_path))  # Bookmark tool
        toolbar.AddStretchableSpace()  # Add stretchable space to the right
        disconnect_tool = toolbar.AddTool(wx.ID_ANY, 'Disconnect', wx.Bitmap(disconnect_icon_path))

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.on_open_connection, ftp_tool)
        self.Bind(wx.EVT_TOOL, self.on_refresh, refresh_tool)
        self.Bind(wx.EVT_TOOL, self.on_disconnect, disconnect_tool)
        self.Bind(wx.EVT_TOOL, self.on_upload, upload_tool)
        self.Bind(wx.EVT_TOOL, self.on_history, history_tool)  # Bind history tool
        self.Bind(wx.EVT_TOOL, self.on_bookmarks, bookmark_tool)  # Bind bookmark tool
        self.Bind(wx.EVT_TOOL, self.on_delete, delete_tool)
        self.Bind(wx.EVT_TOOL, self.on_sftp, sftp_tool)  # Bind SFTP tool

        # Bind the new tools (drive and sftp) to their respective handlers (if needed)
        self.Bind(wx.EVT_TOOL, self.on_drive, drive_tool)
        self.Bind(wx.EVT_TOOL, self.on_sftp, sftp_tool)

    def on_drive(self, event):
        wx.MessageBox('Drive functionality not implemented yet', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_sftp(self, event):
        dlg = SftpDialog(self, 'Open SFTP Connection')
        if dlg.ShowModal() == wx.ID_OK:
            server = dlg.server.GetValue()
            port = dlg.port.GetValue()
            username = dlg.username.GetValue()
            password = dlg.password.GetValue()
            save_password = dlg.save_password.GetValue()

            sftp_info = {
                'host': server,
                'port': port,
                'username': username,
                'password': password if save_password else ''
            }

            save_sftp_server_info(sftp_info)

            threading.Thread(target=self.connect_sftp, args=(server, port, username, password, save_password)).start()

        dlg.Destroy()

    def connect_sftp(self, host, port, username, password, save_password):
        try:
            transport = paramiko.Transport((host, int(port)))
            transport.connect(username=username, password=password)
            self.sftp = paramiko.SFTPClient.from_transport(transport)
            self.current_path = "."
            wx.CallAfter(self.update_sftp_file_list)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Connection Error', wx.OK | wx.ICON_ERROR)

    def update_sftp_file_list(self):
        try:
            files = self.sftp.listdir_attr(self.current_path)
            file_details = [(f.filename, f.st_size, 'Folder' if f.st_mode & 0o040000 else 'File', datetime.datetime.fromtimestamp(f.st_mtime).strftime('%Y-%m-%d %H:%M:%S')) for f in files]
            wx.CallAfter(self.populate_file_list, file_details)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Error Listing Files', wx.OK | wx.ICON_ERROR)

    def create_file_list(self, panel, vbox):
        self.file_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.file_list.InsertColumn(0, 'Filename')
        self.file_list.InsertColumn(1, 'Size', wx.LIST_FORMAT_RIGHT)
        self.file_list.InsertColumn(2, 'Type', wx.LIST_FORMAT_RIGHT)
        self.file_list.InsertColumn(3, 'Date Modified', wx.LIST_FORMAT_RIGHT)
        self.file_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)
        self.file_list.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu)

        # Create an image list and add folder icon
        self.image_list = wx.ImageList(16, 16)
        folder_icon_path = os.path.join(os.getcwd(), 'icons', 'folder.png')
        self.folder_icon_index = self.image_list.Add(wx.Bitmap(folder_icon_path))
        self.file_list.AssignImageList(self.image_list, wx.IMAGE_LIST_SMALL)

        vbox.Add(self.file_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Set column widths based on proportions
        total_width = panel.GetSize().GetWidth()
        self.file_list.SetColumnWidth(0, int(total_width * 0.50))  # Filename (60%)
        self.file_list.SetColumnWidth(1, int(total_width * 0.15))  # Size (15%)
        self.file_list.SetColumnWidth(2, int(total_width * 0.15))  # Type (15%)
        self.file_list.SetColumnWidth(3, int(total_width * 0.2))  # Date Modified (10%)

        # Set the drop target for file_list
        self.file_list.SetDropTarget(FileDropTarget(self))

    def on_size(self, event):
        self.Layout()
        total_width = self.file_list.GetSize().GetWidth()
        self.file_list.SetColumnWidth(0, int(total_width * 0.50))  # Filename (50%)
        self.file_list.SetColumnWidth(1, int(total_width * 0.15))  # Size (15%)
        self.file_list.SetColumnWidth(2, int(total_width * 0.15))  # Type (15%)
        self.file_list.SetColumnWidth(3, int(total_width * 0.2))  # Date Modified (20%)
        event.Skip()

    def update_status_bar(self):
        item_count = self.file_list.GetItemCount()
        self.SetStatusText(f"Items in file list: {item_count}")

    def on_open_connection(self, event):
        dlg = FtpDialog(self, 'Open Connection')
        if dlg.ShowModal() == wx.ID_OK:
            server = dlg.server.GetValue()
            port = dlg.port.GetValue()
            username = dlg.username.GetValue()
            password = dlg.password.GetValue()
            anonymous_login = dlg.anonymous_login.GetValue()
            save_password = dlg.save_password.GetValue()

            server_info = {
                'host': server,
                'port': port,
                'username': username,
                'password': password if save_password else '',
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            save_ftp_server_info(server_info)

            threading.Thread(target=self.connect_ftp, args=(server, port, username, password, anonymous_login, save_password)).start()

        dlg.Destroy()

    def connect_ftp(self, host, port, username, password, anonymous_login, save_password):
        try:
            self.ftp = FTP()
            self.ftp.connect(host, int(port), timeout=10)  # Add a timeout to avoid long waits
            if anonymous_login:
                self.ftp.login()
            else:
                self.ftp.login(username, password)
            self.current_path = "/"
            wx.CallAfter(self.update_file_list)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Connection Error', wx.OK | wx.ICON_ERROR)

    def update_file_list(self):
        normalized_path = os.path.normpath(self.current_path)  # Normalize the path
        if normalized_path in self.cached_files:
            self.populate_file_list(self.cached_files[normalized_path])
        else:
            threading.Thread(target=self.fetch_file_list).start()

    def fetch_file_list(self):
        try:
            self.ftp.cwd(self.current_path)
            files = self.ftp.nlst()
            file_details = []
            for filename in files:
                try:
                    size = self.get_file_size(filename)
                    file_type = 'Folder' if self.is_directory(filename) else 'File'
                    date_modified = '2024-05-16'  # Placeholder, use actual date if needed
                    file_details.append((filename, size, file_type, date_modified))
                except Exception as e:
                    # Handle or log the exception for the specific file
                    continue
            if not file_details:
                pass
            normalized_path = os.path.normpath(self.current_path)  # Normalize the path
            self.cached_files[normalized_path] = file_details
            wx.CallAfter(self.populate_file_list, file_details)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Error Listing Files', wx.OK | wx.ICON_ERROR)

    def populate_file_list(self, file_details):
        self.file_list.DeleteAllItems()
        if self.current_path != "/":
            self.file_list.InsertItem(0, "...")
        for idx, (filename, size, file_type, date_modified) in enumerate(file_details, start=1 if self.current_path != "/" else 0):
            index = self.file_list.InsertItem(idx, filename)
            if file_type == 'Folder':
                self.file_list.SetItemImage(index, self.folder_icon_index)
            else:
                self.file_list.SetItemImage(index, -1)  # -1 means no image
            self.file_list.SetItem(index, 1, size)
            self.file_list.SetItem(index, 2, file_type)
            self.file_list.SetItem(index, 3, date_modified)
        self.update_status_bar()

    def is_directory(self, filename):
        current = self.ftp.pwd()
        try:
            self.ftp.cwd(filename)
            self.ftp.cwd(current)
            return True
        except Exception:
            return False

    def get_file_size(self, filename):
        size = 'N/A'
        try:
            size = self.ftp.size(filename)
            size = f"{size} bytes" if size else 'N/A'
        except:
            pass
        return size

    def get_file_permissions(self, filename):
        try:
            # The LIST command provides details about the file, including permissions
            lines = []
            self.ftp.retrlines(f'LIST {filename}', lines.append)
            if lines:
                return lines[0].split()[0]
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Error Getting Permissions', wx.OK | wx.ICON_ERROR)
        return '----------'

    def set_file_permissions(self, filename, permissions):
        try:
            mode = 0
            if permissions['read']:
                mode += 0o400
            if permissions['write']:
                mode += 0o200
            if permissions['execute']:
                mode += 0o100
            self.ftp.voidcmd(f'SITE CHMOD {mode:o} {filename}')
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Error Setting Permissions', wx.OK | wx.ICON_ERROR)

    def on_item_activated(self, event):
        selected_item = event.GetText()
        if selected_item == "...":
            self.current_path = os.path.dirname(self.current_path.rstrip('/'))
            if not self.current_path:
                self.current_path = "/"
            self.update_file_list()
        elif self.is_directory(selected_item):
            self.current_path = os.path.join(self.current_path, selected_item)
            self.update_file_list()
        else:
            wx.MessageBox(f'Cannot open {selected_item} as it is not a directory', 'Error', wx.OK | wx.ICON_ERROR)

    def on_context_menu(self, event):
        menu = wx.Menu()
        refresh_item = menu.Append(wx.ID_REFRESH, 'Refresh')
        info_item = menu.Append(wx.ID_ANY, 'Info')  # Info seçeneği eklendi
        download_item = menu.Append(wx.ID_ANY, 'Download')
        download_as_item = menu.Append(wx.ID_ANY, 'Download As')
        upload_item = menu.Append(wx.ID_ANY, 'Upload')
        delete_item = menu.Append(wx.ID_ANY, 'Delete')
        rename_item = menu.Append(wx.ID_ANY, 'Rename')

        self.Bind(wx.EVT_MENU, self.on_refresh, refresh_item)
        self.Bind(wx.EVT_MENU, self.on_info, info_item)  # Info işlemi için binding
        self.Bind(wx.EVT_MENU, self.on_download, download_item)
        self.Bind(wx.EVT_MENU, self.on_download_as, download_as_item)
        self.Bind(wx.EVT_MENU, self.on_upload, upload_item)
        self.Bind(wx.EVT_MENU, self.on_delete, delete_item)
        self.Bind(wx.EVT_MENU, self.on_rename, rename_item)

        self.PopupMenu(menu)
        menu.Destroy()

    def on_info(self, event):
        selected_item = self.file_list.GetFirstSelected()
        if selected_item != -1:
            filename = self.file_list.GetItemText(selected_item)
            raw_permissions = self.get_file_permissions(filename)
            permissions = {
                'read': raw_permissions[1] == 'r',
                'write': raw_permissions[2] == 'w',
                'execute': raw_permissions[3] == 'x'
            }

            dlg = InfoDialog(self, f'Info - {filename}', permissions)
            if dlg.ShowModal() == wx.ID_OK:
                # Save the updated permissions
                updated_permissions = dlg.permissions
                threading.Thread(target=self.set_file_permissions, args=(filename, updated_permissions)).start()
            dlg.Destroy()

    def on_download_as(self, event):
        selected_item = self.file_list.GetFirstSelected()
        if selected_item != -1:
            filename = self.file_list.GetItemText(selected_item)
            with wx.FileDialog(self, "Save file as", defaultFile=filename, wildcard="All files (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # User cancelled the dialog

                # Save the selected file
                local_filename = fileDialog.GetPath()
                threading.Thread(target=self.download_file_as, args=(filename, local_filename)).start()

    def download_file_as(self, remote_filename, local_filename):
        def start_download():
            try:
                with open(local_filename, 'wb') as f:
                    def callback(data):
                        f.write(data)

                    self.ftp.retrbinary(f'RETR {remote_filename}', callback)

                wx.CallAfter(lambda: on_download_complete(True, remote_filename, local_filename))
            except Exception as e:
                wx.CallAfter(lambda: on_download_complete(False, str(e)))

        def on_download_complete(success, *args):
            if success:
                wx.MessageBox(f'Downloaded {args[0]} to {args[1]}', 'Info', wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox(f'Download Error: {args[0]}', 'Error', wx.OK | wx.ICON_ERROR)

        threading.Thread(target=start_download).start()

    def on_download(self, event):
        selected_item = self.file_list.GetFirstSelected()
        if selected_item != -1:
            filename = self.file_list.GetItemText(selected_item)
            downloads_path = os.path.expanduser("~/Downloads")
            local_filename = os.path.join(downloads_path, filename)
            threading.Thread(target=self.download_file, args=(filename, local_filename)).start()

    def download_file(self, remote_filename, local_filename):
        def start_download():
            try:
                with open(local_filename, 'wb') as f:
                    def callback(data):
                        f.write(data)

                    self.ftp.retrbinary(f'RETR {remote_filename}', callback)

                wx.CallAfter(lambda: on_download_complete(True, remote_filename, local_filename))
            except Exception as e:
                wx.CallAfter(lambda: on_download_complete(False, str(e)))

        def on_download_complete(success, *args):
            if success:
                wx.MessageBox(f'Downloaded {args[0]} to {args[1]}', 'Info', wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox(f'Download Error: {args[0]}', 'Error', wx.OK | wx.ICON_ERROR)

        threading.Thread(target=start_download).start()

    def on_upload(self, event):
        with wx.FileDialog(self, "Upload file", wildcard="All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_MULTIPLE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            paths = fileDialog.GetPaths()
            for path in paths:
                threading.Thread(target=self.upload_file, args=(path,)).start()

    def upload_file(self, local_filename):
        def start_upload():
            try:
                with open(local_filename, 'rb') as f:
                    self.ftp.storbinary(f'STOR {os.path.basename(local_filename)}', f)

                del self.cached_files[os.path.normpath(self.current_path)]  # Clear cache
                wx.CallAfter(self.update_file_list)
                wx.CallAfter(lambda: on_upload_complete(True, local_filename))
            except Exception as e:
                wx.CallAfter(lambda: on_upload_complete(False, str(e)))

        def on_upload_complete(success, *args):
            if success:
                wx.MessageBox(f'Uploaded {args[0]}', 'Info', wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox(f'Upload Error: {args[0]}', 'Error', wx.OK | wx.ICON_ERROR)

        threading.Thread(target=start_upload).start()

    def on_rename(self, event):
        selected_item = self.file_list.GetFirstSelected()
        if selected_item != -1:
            filename = self.file_list.GetItemText(selected_item)

            # Open a dialog to get the new name
            dlg = wx.TextEntryDialog(self, f'Enter new name for {filename}:', 'Rename File', value=filename)

            if dlg.ShowModal() == wx.ID_OK:
                new_name = dlg.GetValue()
                threading.Thread(target=self.rename_file, args=(filename, new_name)).start()

            dlg.Destroy()

    def rename_file(self, old_name, new_name):
        try:
            self.ftp.rename(old_name, new_name)
            del self.cached_files[os.path.normpath(self.current_path)]  # Clear cache
            wx.CallAfter(self.update_file_list)
            wx.CallAfter(wx.MessageBox, f'Renamed {old_name} to {new_name}', 'Info', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Rename Error', wx.OK | wx.ICON_ERROR)

    def on_delete(self, event):
        selected_item = self.file_list.GetFirstSelected()
        if selected_item != -1:
            filename = self.file_list.GetItemText(selected_item)
            confirm_dialog = wx.MessageDialog(None, f"Are you sure you want to delete '{filename}'?", "Confirm Deletion", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            if confirm_dialog.ShowModal() == wx.ID_YES:
                threading.Thread(target=self.delete_file, args=(filename,)).start()

    def delete_file(self, filename):
        try:
            if self.is_directory(filename):
                self.ftp.rmd(filename)
            else:
                self.ftp.delete(filename)
            del self.cached_files[os.path.normpath(self.current_path)]  # Clear cache
            wx.CallAfter(self.update_file_list)
            wx.CallAfter(wx.MessageBox, f'Deleted {filename}', 'Info', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Delete Error', wx.OK | wx.ICON_ERROR)

    def on_disconnect(self, event):
        if self.ftp:
            try:
                self.ftp.quit()
            except (ConnectionResetError, error_perm):
                pass
            self.ftp = None
        if self.sftp:  # SFTP bağlantısı için ekleme
            try:
                self.sftp.close()
            except Exception:
                pass
            self.sftp = None

        self.file_list.DeleteAllItems()  # Clear the file list
        self.cached_files.clear()  # Clear the cache
        self.current_path = "/"  # Reset the current path
        self.update_status_bar()  # Update the status bar
        wx.MessageBox('Disconnected from server', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_refresh(self, event):
        if self.ftp:
            normalized_path = os.path.normpath(self.current_path)  # Normalize the path
            if normalized_path in self.cached_files:
                del self.cached_files[normalized_path]  # Clear cache
            threading.Thread(target=self.fetch_file_list_with_message).start()
        elif self.sftp:
            threading.Thread(target=self.update_sftp_file_list_with_message).start()

    def fetch_file_list_with_message(self):
        try:
            self.fetch_file_list()
            wx.CallAfter(wx.MessageBox, 'File list has been refreshed.', 'Refresh Complete', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Error Listing Files', wx.OK | wx.ICON_ERROR)

    def update_sftp_file_list_with_message(self):
        try:
            self.update_sftp_file_list()
            wx.CallAfter(wx.MessageBox, 'SFTP file list has been refreshed.', 'Refresh Complete', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, str(e), 'Error Listing Files', wx.OK | wx.ICON_ERROR)

    def on_about(self, event):
        wx.MessageBox('PyStreamFiler (PSF) is a Python-based file transfer and cloud storage manager, simplifying data handling across FTP, SFTP, and WebDAV. As an open-source, community-backed project, it emphasizes secure, user-friendly operations and seamless integration with various cloud services. Designed for easy file management and synchronization.\nBy Ali Duman, Dilara Akdeniz, Zeynep Başoğlu', 'About FTP Client', wx.OK | wx.ICON_INFORMATION)

    def on_history(self, event):
        dlg = HistoryDialog(self, 'Connection History')
        dlg.ShowModal()
        dlg.Destroy()

    def on_bookmarks(self, event):
        dlg = BookmarksDialog(self, 'Bookmarks')
        dlg.ShowModal()
        dlg.Destroy()

    def on_new_browser(self, event):
        new_frame = FTPClientFrame(None, 'PSF - New Browser')
        new_frame.Show()

    def on_back(self, event):
        wx.MessageBox('Back functionality', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_forward(self, event):
        wx.MessageBox('Forward functionality', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_up(self, event):
        wx.MessageBox('Up functionality', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_add_bookmark(self, event):
        dlg = FtpDialog(self, 'Add Bookmark')
        if dlg.ShowModal() == wx.ID_OK:
            server = dlg.server.GetValue()
            port = dlg.port.GetValue()
            username = dlg.username.GetValue()
            password = dlg.password.GetValue()
            anonymous_login = dlg.anonymous_login.GetValue()
            save_password = dlg.save_password.GetValue()

            bookmark_info = {
                'host': server,
                'port': port,
                'username': username,
                'password': password if save_password else '',
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            save_bookmark_info(bookmark_info)

        dlg.Destroy()

    def on_manage_bookmarks(self, event):
        dlg = BookmarksDialog(self, 'Manage Bookmarks')
        dlg.ShowModal()
        dlg.Destroy()

    def on_new_window(self, event):
        new_frame = FTPClientFrame(None, 'PSF - New Window')
        new_frame.Show()

    def on_close_window(self, event):
        self.Close()

    def on_cut(self, event):
        wx.MessageBox('Cut functionality', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_copy(self, event):
        wx.MessageBox('Copy functionality', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_paste(self, event):
        wx.MessageBox('Paste functionality', 'Info', wx.OK | wx.ICON_INFORMATION)

    def close_ftp(self):
        if self.ftp:
            try:
                self.ftp.quit()
            except (ConnectionResetError, error_perm):
                pass

    def close_sftp(self):  # SFTP bağlantısını kapatma fonksiyonu
        if self.sftp:
            try:
                self.sftp.close()
            except Exception:
                pass

    def OnQuit(self, event):
        self.close_ftp()
        self.close_sftp()  # SFTP bağlantısını kapatma
        self.Close()


def save_ftp_server_info(server_info):
    file_path = "ftp_server_info.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    # Sunucu bilgisine zaman damgası ekle
    server_info['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Yinelenenleri kaldır
    data = [item for item in data if (item['host'], item['port'], item['username']) != (server_info['host'], server_info['port'], server_info['username'])]

    # Yeni bağlantıyı listenin başına ekle
    data.insert(0, server_info)

    with open(file_path, "w") as file:
        json.dump(data, file)


def load_ftp_server_info():
    file_path = "ftp_server_info.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []


def save_sftp_server_info(server_info):
    file_path = "sftp_server_info.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    # Sunucu bilgisine zaman damgası ekle
    server_info['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Yinelenenleri kaldır
    data = [item for item in data if (item['host'], item['port'], item['username']) != (server_info['host'], server_info['port'], server_info['username'])]

    # Yeni bağlantıyı listenin başına ekle
    data.insert(0, server_info)

    with open(file_path, "w") as file:
        json.dump(data, file)


def load_sftp_server_info():
    file_path = "sftp_server_info.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []


def save_bookmark_info(bookmark_info):
    file_path = "bookmarks_info.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    # Yinelenenleri kaldır
    data = [item for item in data if (item['host'], item['port'], item['username']) != (bookmark_info['host'], bookmark_info['port'], bookmark_info['username'])]

    # Yeni yer imini listenin başına ekle
    data.insert(0, bookmark_info)

    with open(file_path, "w") as file:
        json.dump(data, file)


def load_bookmark_info():
    file_path = "bookmarks_info.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []


def main():
    app = wx.App(False)
    frame = FTPClientFrame(None, 'PSF')
    app.MainLoop()


if __name__ == '__main__':
    main()
