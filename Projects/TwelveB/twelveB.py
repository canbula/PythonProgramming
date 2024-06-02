import wx
import sqlite3

class NotionApp(wx.Frame):
    def __init__(self, user_id, *args, **kwargs):
        super(NotionApp, self).__init__(*args, **kwargs)
        self.dark_mode = self.load_dark_mode_state()
        self.init_ui()
        self.conn = sqlite3.connect("registered.db")
        self.create_tables()
        self.user_id = user_id  # Oturum açmış kullanıcı ID'si burada saklanıyor
        self.show_notes()

    def load_dark_mode_state(self):
        try:
            with open("dark_mode.txt", "r") as file:
                return file.read().strip() == "True"
        except FileNotFoundError:
            return False

    def toggle_dark_mode(self, event):
        self.dark_mode = not self.dark_mode
        self.apply_dark_mode()
        self.save_dark_mode_state_to_db()

    def save_dark_mode_state_to_db(self):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE settings SET dark_mode = ? WHERE id = 1", (int(self.dark_mode),))
        self.conn.commit()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                note TEXT,
                checked INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                dark_mode INTEGER
            )
        ''')
        self.conn.commit()

    def init_ui(self):
        self.SetTitle("Welcome to TwelveB")
        self.SetSize((500, 400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.listbox = wx.CheckListBox(panel)
        vbox.Add(self.listbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.text_ctrl = wx.TextCtrl(panel)
        hbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND)
        add_button = wx.Button(panel, label="Ekle")
        add_button.Bind(wx.EVT_BUTTON, self.on_add)
        hbox.Add(add_button, flag=wx.LEFT, border=5)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)

        delete_button = wx.Button(panel, label="Sil")
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete)
        vbox.Add(delete_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)

        edit_button = wx.Button(panel, label="Düzenle")
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        vbox.Add(edit_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)

        exit_button = wx.Button(panel, label="Hesap Değiştir")
        exit_button.Bind(wx.EVT_BUTTON, self.on_exit)
        vbox.Add(exit_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)

        dark_mode_button = wx.Button(panel, label="Dark Mode")
        dark_mode_button.Bind(wx.EVT_BUTTON, self.toggle_dark_mode)
        vbox.Add(dark_mode_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_CHECKLISTBOX, self.on_check)

    def apply_dark_mode(self):
        # Dark mode aktifse arayüz renklerini değiştir
        if self.dark_mode:
            self.SetBackgroundColour(wx.Colour(25, 25, 25))  # Arka plan rengini değiştir
            self.listbox.SetBackgroundColour(wx.Colour(25, 25, 25))  # Liste kutusunun arka plan rengini değiştir
            self.listbox.SetForegroundColour(wx.Colour(500, 500, 500))  # Liste kutusunun metin rengini değiştir
        else:
            self.SetBackgroundColour(wx.NullColour)  # Arka plan rengini varsayılana ayarla
            self.listbox.SetBackgroundColour(wx.NullColour)  # Liste kutusunun arka plan rengini varsayılana ayarla
            self.listbox.SetForegroundColour(wx.NullColour)  # Liste kutusunun metin rengini varsayılana ayarla

        self.Refresh()  # Arayüzün yenilenmesini sağla

    def show_notes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT note, checked FROM notes WHERE user_id=?", (self.user_id,))
        notes = cursor.fetchall()

        self.listbox.Clear()
        for note, checked in notes:
            self.listbox.Append(note)
            if checked:
                self.listbox.Check(self.listbox.GetCount() - 1)

    def get_current_user_id(self):
        return self.user_id

    def on_add(self, event):
        item = self.text_ctrl.GetValue()
        if item:
            user_id = self.get_current_user_id()  # Kullanıcının ID'sini almak için bir yol bulunmalıdır
            self.add_note(user_id, item)  # Önce veritabanına ekleyin
            self.show_notes()  # Notları tekrar yükleyin
            self.text_ctrl.Clear()

    def on_edit(self, event):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            current_note = self.listbox.GetString(selection)
            dialog = wx.TextEntryDialog(self, "Notu Düzenle:", "Not Düzenleme")
            dialog.SetValue(current_note)  # Varsayılan değeri ayarla
            if dialog.ShowModal() == wx.ID_OK:
                new_note = dialog.GetValue()
                if new_note and new_note != current_note:
                    self.edit_note(current_note, new_note)
                    self.show_notes()
            dialog.Destroy()

    def edit_note(self, current_note, new_note):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE notes SET note=? WHERE user_id=? AND note=?", (new_note, self.user_id, current_note))
        self.conn.commit()

    def add_note(self, user_id, note):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO notes (user_id, note, checked) VALUES (?, ?, 0)", (user_id, note))
        self.conn.commit()
        print("Not kaydedildi:", note)

    def on_delete(self, event):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            note = self.listbox.GetString(selection)
            self.delete_note(note)
            self.show_notes()

    def delete_note(self, note):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notes WHERE user_id=? AND note=?", (self.user_id, note))
        self.conn.commit()

    def on_exit(self, event):
        self.Close(True)  # Uygulamayı kapat
        app = wx.GetApp()
        login_dialog = LoginDialog(None)
        login_dialog.ShowModal()

    def on_check(self, event):
        index = event.GetInt()
        note = self.listbox.GetString(index)
        checked = self.listbox.IsChecked(index)

        cursor = self.conn.cursor()
        cursor.execute("UPDATE notes SET checked=? WHERE user_id=? AND note=?", (int(checked), self.user_id, note))
        self.conn.commit()
        print(f"Updated note '{note}' to {'checked' if checked else 'unchecked'}.")

class LoginDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.SetTitle("Giriş Yap")
        self.SetSize((400, 400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        username_label = wx.StaticText(panel, label="Kullanıcı Adı:")
        vbox.Add(username_label, flag=wx.LEFT | wx.TOP, border=10)
        self.username_textctrl = wx.TextCtrl(panel)
        vbox.Add(self.username_textctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        password_label = wx.StaticText(panel, label="Şifre:")
        vbox.Add(password_label, flag=wx.LEFT | wx.TOP, border=10)
        self.password_textctrl = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        vbox.Add(self.password_textctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        login_button = wx.Button(panel, label="Giriş Yap")
        login_button.Bind(wx.EVT_BUTTON, self.on_login)
        vbox.Add(login_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        forgot_button = wx.Button(panel, label="Şifremi Unuttum")
        forgot_button.Bind(wx.EVT_BUTTON, self.on_forgot_password)
        vbox.Add(forgot_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        register_button = wx.Button(panel, label="Kayıt Ol")
        register_button.Bind(wx.EVT_BUTTON, self.on_register)
        vbox.Add(register_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, border=10)

        exit_application_button = wx.Button(panel, label="Uygulamayı Kapat")
        exit_application_button.Bind(wx.EVT_BUTTON, self.on_exit_application)
        vbox.Add(exit_application_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def on_exit_application(self, event):
        self.Destroy()  # Uygulama penceresini kapat
        app = wx.GetApp()
        app.ExitMainLoop()  # Uygulamanın çalışmasını durdur

    def on_forgot_password(self, event):
        username = wx.GetTextFromUser("Lütfen kullanıcı adınızı girin:", "Şifremi Unuttum")
        if username:
            conn = sqlite3.connect("registered.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            if user:
                wx.MessageBox(f"Şifreniz: {user[0]}", "Şifreniz", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("Kullanıcı adı bulunamadı!", "Hata", wx.OK | wx.ICON_ERROR)

    def on_register(self, event):
        register_dialog = RegisterDialog(None)
        if register_dialog.ShowModal() == wx.ID_OK:
            wx.MessageBox("Kayıt başarıyla tamamlandı! Lütfen giriş yapın.", "Başarılı", wx.OK | wx.ICON_INFORMATION)

    def on_login(self, event):
        def login(username, password):
            conn = sqlite3.connect("registered.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                return user[0]
            else:
                return None

        username = self.username_textctrl.GetValue()
        password = self.password_textctrl.GetValue()
        user_id = login(username, password)
        if user_id is not None:
            app = wx.GetApp()
            app.frame = NotionApp(user_id, None)
            app.frame.show_notes()  # Kullanıcının notlarını göster
            app.frame.Show()
            self.Destroy()
        else:
            wx.MessageBox("Kullanıcı adı veya şifre yanlış!", "Hata", wx.OK | wx.ICON_ERROR)
            self.username_textctrl.Clear()
            self.password_textctrl.Clear()

    def on_register(self, event):
        register_dialog = RegisterDialog(None)
        if register_dialog.ShowModal() == wx.ID_OK:
            wx.MessageBox("Kayıt başarıyla tamamlandı! Lütfen giriş yapın.", "Başarılı", wx.OK | wx.ICON_INFORMATION)

class RegisterDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(RegisterDialog, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.SetTitle("Kayıt Ol")
        self.SetSize((350, 200))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        username_label = wx.StaticText(panel, label="Kullanıcı Adı:")
        vbox.Add(username_label, flag=wx.LEFT | wx.TOP, border=10)
        self.username_textctrl = wx.TextCtrl(panel)
        vbox.Add(self.username_textctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        password_label = wx.StaticText(panel, label="Şifre:")
        vbox.Add(password_label, flag=wx.LEFT | wx.TOP, border=10)
        self.password_textctrl = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        vbox.Add(self.password_textctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        register_button = wx.Button(panel, label="Kayıt Ol")
        register_button.Bind(wx.EVT_BUTTON, self.on_register)
        vbox.Add(register_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def on_register(self, event):
        username = self.username_textctrl.GetValue()
        password = self.password_textctrl.GetValue()
        if username and password:
            conn = sqlite3.connect("registered.db")  # Veritabanı burada açılıyor
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()  # Veritabanı burada kapanıyor
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox("Kullanıcı adı ve şifre boş bırakılamaz!", "Hata", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App()
    login_dialog = LoginDialog(None)
    login_dialog.ShowModal()
    app.MainLoop()