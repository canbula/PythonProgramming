import wx
import wx.grid
from db import Firebase
from professor import Professor
from course import Course
import random
import string
import time
import csv
import os


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


class CoursesPanel(wx.Panel):
    def __init__(self, parent, title, professor: Professor, f: Firebase):
        super(CoursesPanel, self).__init__(parent)

        self.f = f
        self.professor = professor

        self.init_ui()

    def init_ui(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.courses_label = wx.StaticText(
            self, label="Courses", style=wx.ALIGN_CENTER, size=(200, 20)
        )

        self.courses_grid = wx.grid.Grid(self, size=(700, 150))

        self.setup_grid()

        self.new_course_panel = wx.Panel(self)
        self.new_course_sizer = wx.GridBagSizer(10, 10)

        self.title_label = wx.StaticText(
            self.new_course_panel, label="Title", style=wx.ALIGN_LEFT, size=(60, 20)
        )
        self.title_entry = wx.TextCtrl(
            self.new_course_panel, size=(200, 20), style=wx.TE_LEFT
        )
        self.description_label = wx.StaticText(
            self.new_course_panel,
            label="Description",
            style=wx.ALIGN_LEFT,
            size=(80, 20),
        )
        self.description_entry = wx.TextCtrl(
            self.new_course_panel, size=(200, 20), style=wx.TE_LEFT
        )

        self.add_course_button = wx.Button(self.new_course_panel, label="Add Course")
        self.add_course_button.Bind(wx.EVT_BUTTON, self.on_add_course)

        self.new_course_sizer.Add(
            self.title_label, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL
        )
        self.new_course_sizer.Add(self.title_entry, pos=(0, 1), flag=wx.EXPAND)
        self.new_course_sizer.Add(
            self.description_label, pos=(0, 2), flag=wx.ALIGN_CENTER_VERTICAL
        )
        self.new_course_sizer.Add(self.description_entry, pos=(0, 3), flag=wx.EXPAND)
        self.new_course_sizer.AddGrowableCol(1)
        self.new_course_sizer.Add(
            self.add_course_button, pos=(0, 4), span=(1, 2), flag=wx.ALIGN_RIGHT
        )

        self.new_course_panel.SetSizer(self.new_course_sizer)

        self.sizer.Add(self.courses_label, 0, wx.CENTER)
        self.sizer.Add(self.courses_grid, 0, wx.CENTER)
        self.sizer.Add((-1, 10))
        self.sizer.Add(self.new_course_panel, 0, wx.CENTER)

        self.attance_code_panel = wx.Panel(self)
        self.attendance_code_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.course_label = wx.StaticText(
            self.attance_code_panel, label="Course", style=wx.ALIGN_LEFT, size=(60, 20)
        )
        self.course_dropdown = wx.Choice(self.attance_code_panel, size=(200, 20))
        self.course_dropdown.AppendItems(["Select Course"])
        self.course_dropdown.SetSelection(0)
        self.load_courses_to_dropdown()
        self.attendance_code_sizer.Add(self.course_label, 0, wx.ALIGN_CENTER_VERTICAL)
        self.course_dropdown.Bind(wx.EVT_CHOICE, self.on_course_choice)

        self.generate_code_button = wx.Button(
            self.attance_code_panel, label="Generate Attendance Code"
        )
        self.attendance_code_sizer.Add(self.course_dropdown, 0, wx.EXPAND)
        self.generate_code_button.Bind(wx.EVT_BUTTON, self.on_generate_code)
        self.attendance_code_sizer.Add((10, -1))
        self.attendance_code_sizer.Add(self.generate_code_button, 0, wx.EXPAND)

        self.attendance_code_sizer.Add((10, -1))
        self.attendance_code_sizer.Add(self.download_report_button, 0, wx.EXPAND)

        self.attance_code_panel.SetSizer(self.attendance_code_sizer)

        self.sizer.Add((-1, 10))
        self.sizer.Add(self.attance_code_panel, 0, wx.CENTER)

        self.SetSizer(self.sizer)

    def load_courses_to_dropdown(self):
        courses = self.f.ref.child("courses").get()
        if courses:
            for course in courses:
                if courses[course]["user_id"] == self.professor.user_id:
                    self.course_dropdown.Append(courses[course]["title"])

    def on_course_choice(self, event):
        print(self.course_dropdown.GetStringSelection())

    def on_generate_code(self, event):
        print("Generating attendance code...")
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        print(f"Attendance code: {code}")
        self.save_attendance_code(code, self.course_dropdown.GetStringSelection())
        wx.MessageBox(
            f"Attendance code for {self.course_dropdown.GetStringSelection()} is {code}",
            "Attendance Code",
            wx.OK | wx.ICON_INFORMATION,
        )

    def save_attendance_code(self, code, course_title):
        courses = self.f.ref.child("courses").get()
        if courses:
            for course in courses:
                if courses[course]["title"] == course_title:
                    course_id = str(course)
                    valid_until = time.time() + 3 * 60
                    self.f.ref.child("attendance_codes").child(course_id).set(
                        {
                            "code": code,
                            "valid_until": valid_until,
                        }
                    )
                    print(f"Attendance code for {course_title} is {code}")
                    print(f"Valid until: {time.ctime(valid_until)}")

    def setup_grid(self):
        self.courses_grid.CreateGrid(0, 2)
        self.courses_grid.SetColLabelValue(0, "Title")
        self.courses_grid.SetColLabelValue(1, "Description")
        self.courses_grid.SetRowLabelSize(0)
        self.courses_grid.SetColSize(0, 250)
        self.courses_grid.SetColSize(1, 450)
        self.load_courses()

    def load_courses(self):
        self.courses_grid.ClearGrid()
        if self.courses_grid.GetNumberRows() > 0:
            self.courses_grid.DeleteRows(0, self.courses_grid.GetNumberRows())
        courses = self.f.ref.child("courses").get()
        if courses:
            i = 0
            for course in enumerate(courses):
                if courses[course]["user_id"] == self.professor.user_id:
                    self.courses_grid.AppendRows(1)
                    self.courses_grid.SetCellValue(i, 0, courses[course]["title"])
                    self.courses_grid.SetCellValue(i, 1, courses[course]["description"])
                    i += 1

    def on_add_course(self, event):
        course = Course(self.professor.user_id, self.f)
        course.title = self.title_entry.GetValue()
        course.description = self.description_entry.GetValue()
        course.create()
        self.load_courses()
        self.title_entry.SetValue("")
        self.description_entry.SetValue("")


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

        courses_panel = CoursesPanel(
            panel,
            title="Courses",
            professor=self.professor,
            f=self.f,
        )

        sizer.Add(welcome_panel, 0, wx.CENTER)
        sizer.Add((-1, 20))
        sizer.Add(professor_panel, 0, wx.CENTER)
        sizer.Add((-1, 20))
        sizer.Add(courses_panel, 0, wx.CENTER)
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
