import wx
import wx.grid
from db import Firebase
from professor import Professor


class LoginFrame(wx.Frame):
    def __init__(self, parent, title, f: Firebase):
        super(LoginFrame, self).__init__(parent, title=title, size=(400, 550))

        self.f = f
        self.user = None

        self.init_ui()
        self.Centre()
        self.Show()

        wx.TopLevelWindow.Bind(self, wx.EVT_CLOSE, self.on_close)
        wx.TopLevelWindow.RequestUserAttention(self, True)

    def init_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add((-1, 10))

        logo = wx.StaticBitmap(panel, bitmap=wx.Bitmap("logo.png"))
        sizer.Add(logo, 0, wx.CENTER)

        email_label = wx.StaticText(
            panel, label="Email", style=wx.ALIGN_CENTER, size=(200, 20)
        )
        self.email_entry = wx.TextCtrl(
            panel, size=(200, 20), style=wx.TE_CENTER, value="prof@university.edu"
        )

        password_label = wx.StaticText(
            panel, label="Password", style=wx.ALIGN_CENTER, size=(200, 20)
        )
        self.password_entry = wx.TextCtrl(
            panel,
            size=(200, 20),
            style=wx.TE_CENTER | wx.TE_PASSWORD,
            value="password",
        )

        login_button = wx.Button(panel, label="Login")
        login_button.Bind(wx.EVT_BUTTON, self.on_login)

        sizer.Add(email_label, 0, wx.CENTER)
        sizer.Add((-1, 10))
        sizer.Add(self.email_entry, 0, wx.CENTER)
        sizer.Add((-1, 10))
        sizer.Add(password_label, 0, wx.CENTER)
        sizer.Add((-1, 10))
        sizer.Add(self.password_entry, 0, wx.CENTER)
        sizer.Add((-1, 10))
        sizer.Add(login_button, 0, wx.CENTER)

        panel.SetSizer(sizer)

    def on_login(self, event):
        email = self.email_entry.GetValue()
        password = self.password_entry.GetValue()
        try:
            self.user = self.f.login(email, password)
            print(f"Logged in as {self.f.get_user_email()}")
        except Exception as e:
            self.user = self.f.register(email, password)
            print(f"Registered as {self.f.get_user_email()}")
        self.Close()

    def on_close(self, event):
        self.Destroy()


class ProfessorPanel(wx.Panel):
    def __init__(self, parent, title, professor: Professor, f: Firebase):
        super(ProfessorPanel, self).__init__(parent)

        self.f = f
        self.professor = professor

        self.init_ui()

    def init_ui(self):
        sizer = wx.GridBagSizer(10, 10)

        self.title_label = wx.StaticText(
            self, label="Title", style=wx.ALIGN_LEFT, size=(200, 20)
        )
        self.title_entry = wx.TextCtrl(self, size=(200, 20), style=wx.TE_LEFT)
        self.fullname_label = wx.StaticText(
            self, label="Full Name", style=wx.ALIGN_LEFT, size=(200, 20)
        )
        self.fullname_entry = wx.TextCtrl(self, size=(200, 20), style=wx.TE_LEFT)
        self.department_label = wx.StaticText(
            self, label="Department", style=wx.ALIGN_LEFT, size=(200, 20)
        )
        self.department_entry = wx.TextCtrl(self, size=(200, 20), style=wx.TE_LEFT)
        self.university_label = wx.StaticText(
            self, label="University", style=wx.ALIGN_LEFT, size=(200, 20)
        )
        self.university_entry = wx.TextCtrl(self, size=(200, 20), style=wx.TE_LEFT)

        if self.professor:
            self.title_entry.SetValue(self.professor.title)
            self.fullname_entry.SetValue(self.professor.fullname)
            self.department_entry.SetValue(self.professor.department)
            self.university_entry.SetValue(self.professor.university)

        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        sizer.Add(self.title_label, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.title_entry, pos=(0, 1), flag=wx.EXPAND)
        sizer.Add(self.fullname_label, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.fullname_entry, pos=(1, 1), flag=wx.EXPAND)
        sizer.Add(self.department_label, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.department_entry, pos=(2, 1), flag=wx.EXPAND)
        sizer.Add(self.university_label, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.university_entry, pos=(3, 1), flag=wx.EXPAND)
        sizer.Add(self.save_button, pos=(4, 0), span=(1, 2), flag=wx.ALIGN_RIGHT)

        sizer.AddGrowableCol(1)

        self.SetSizer(sizer)

    def on_save(self, event):
        updates = {
            "title": self.title_entry.GetValue(),
            "fullname": self.fullname_entry.GetValue(),
            "department": self.department_entry.GetValue(),
            "university": self.university_entry.GetValue(),
        }
        self.professor.update(updates)
        print(
            f"Professor {self.professor.fullname} updated successfully with {updates}"
        )


class MainFrame(wx.Frame):
    def __init__(self, parent, title, user, f: Firebase):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 800))

        self.f = f
        self.user = user
        self.professor = Professor(self.f.get_user_id(), self.f)

        self.init_ui()
        self.Centre()
        self.Show()

        wx.TopLevelWindow.Bind(self, wx.EVT_CLOSE, self.on_close)
        wx.TopLevelWindow.RequestUserAttention(self, True)

    def init_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        logo = wx.StaticBitmap(panel, bitmap=wx.Bitmap("logo.png"))
        sizer.Add(logo, 0, wx.CENTER)

        welcome_panel = wx.Panel(panel)
        welcome_sizer = wx.BoxSizer(wx.HORIZONTAL)

        welcome_label = wx.StaticText(
            welcome_panel,
            label=f"Welcome, {self.f.get_user_email()}",
            style=wx.ALIGN_CENTER,
            size=(200, 20),
        )

        logout_button = wx.Button(welcome_panel, label="Logout")
        logout_button.Bind(wx.EVT_BUTTON, self.on_logout)

        welcome_sizer.Add((-1, 10))
        welcome_sizer.Add(welcome_label, 0, wx.CENTER)
        welcome_sizer.Add((-1, 10))
        welcome_sizer.Add(logout_button, 0, wx.CENTER)
        welcome_panel.SetSizer(welcome_sizer)

        professor_panel = ProfessorPanel(
            panel,
            title="Professor",
            professor=self.professor,
            f=self.f,
        )

        sizer.Add(welcome_panel, 0, wx.CENTER)
        sizer.Add((-1, 20))
        sizer.Add(professor_panel, 0, wx.CENTER)
        sizer.Add((-1, 20))
        panel.SetSizer(sizer)

    def on_logout(self, event):
        self.f.logout()
        self.Close()

    def on_close(self, event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    f = Firebase()
    login_frame = LoginFrame(None, title="Login to CAT", f=f)
    app.MainLoop()
    if login_frame.user:
        main_frame = MainFrame(
            None, title="CAT: Classroom Attendance Tracker", user=login_frame.user, f=f
        )
        app.MainLoop()
