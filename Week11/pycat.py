from db import Firebase
import wx  # pip install wxPython


class LoginFrame(wx.Frame):
    def __init__(self, parent, title, f: Firebase):
        super(LoginFrame, self).__init__(parent, title=title, size=(400, 550))

        self.f = f
        self.user = None

        self.init_ui()
        self.Centre()
        self.Show()

    def init_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        logo = wx.StaticBitmap(panel, bitmap=wx.Bitmap("logo.png"))

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
            panel, size=(200, 20), style=wx.TE_PASSWORD | wx.TE_CENTER, value="password"
        )

        login_button = wx.Button(
            panel, label="Login", size=(200, 20), style=wx.ALIGN_CENTER
        )
        login_button.Bind(wx.EVT_BUTTON, self.on_login)

        sizer.Add(-1, 10)
        sizer.Add(logo, 0, wx.ALIGN_CENTER)
        sizer.Add(-1, 10)
        sizer.Add(email_label, 0, wx.ALIGN_CENTER)
        sizer.Add(-1, 10)
        sizer.Add(self.email_entry, 0, wx.ALIGN_CENTER)
        sizer.Add(-1, 10)
        sizer.Add(password_label, 0, wx.ALIGN_CENTER)
        sizer.Add(-1, 10)
        sizer.Add(self.password_entry, 0, wx.ALIGN_CENTER)
        sizer.Add(-1, 20)
        sizer.Add(login_button, 0, wx.ALIGN_CENTER)

        panel.SetSizer(sizer)

    def on_login(self, event):
        email = self.email_entry.GetValue()
        password = self.password_entry.GetValue()
        try:
            self.user = self.f.login(email, password)
            print("Login successful as ", self.user)
        except Exception as e:
            self.user = self.f.register(email, password)
            print("Registration successful as ", self.user)
        self.Close()


if __name__ == "__main__":
    app = wx.App()
    f = Firebase()
    login_frame = LoginFrame(None, title="Login to CAT", f=f)
    app.MainLoop()
