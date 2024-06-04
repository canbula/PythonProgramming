from database import Firebase
import wx  # pip install wxPython
import random 
import wx.grid as gridlib


class NewDatabaseNameFrame(wx.Frame):
    def __init__(self, parent, title, f, user_id, new_database_frame_ref):
        super(NewDatabaseNameFrame, self).__init__(parent, title=title, size=(300, 180))
        self.parent = parent  #We're saving the top window.
        self.f = f  # We're saving the Firebase object.
        self.user_id = user_id  # Retrieve the user ID
        self.new_database_frame_ref = new_database_frame_ref  # Add a reference to the new database window.
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(panel, label="Enter Database Name:")
        self.database_name_entry = wx.TextCtrl(panel)
        save_button = wx.Button(panel, label="Save")
        
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
       

        sizer.Add(label, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.database_name_entry, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(save_button, 0, wx.ALL | wx.CENTER, 5)
        

        panel.SetSizer(sizer)
        panel.SetBackgroundColour(wx.Colour(174,178,233))
       
        self.Centre()
        self.Show()

    def on_save(self, event):
        database_name = self.database_name_entry.GetValue()
        if database_name:
            self.f.create_new_database(database_name)  #Retrieve the user_id parameter from within.
            self.new_database_frame_ref.Show()  # Show the new database window again.
            self.Close()  # Close the current window.
            result_frame = ResultFrame(None, title="Result Frame", f=self.f, user=self.user_id)
            result_frame.Show()

    


class NewDatabaseFrame(wx.Frame):
    def __init__(self, parent, title, f, user_id):
        super(NewDatabaseFrame, self).__init__(parent, title=title, size=(300, 150))
        self.f = f
        self.database_name = None  # Database name
        self.user_id = user_id  # Get the user ID
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        continue_button = wx.Button(panel, label="Continue")
        continue_button.Bind(wx.EVT_BUTTON, self.on_continue)
        continue_button.SetBackgroundColour(wx.Colour(37,47,156))
        continue_button.SetForegroundColour(wx.WHITE)

        new_database_button = wx.Button(panel, label="New Database")
        new_database_button.Bind(wx.EVT_BUTTON, self.on_new_database)
        new_database_button.SetBackgroundColour(wx.Colour(37,47,156))
        new_database_button.SetForegroundColour(wx.WHITE)

        sizer.Add(new_database_button, 0, wx.ALL | wx.CENTER, 5)  # Add the New Database button to your UI.
        sizer.Add(continue_button, 0, wx.ALIGN_CENTER)  # Add the Continue button to your UI.
        panel.SetSizer(sizer)
        panel.SetBackgroundColour(wx.Colour(174,178,233))
        self.Centre()
        self.Show()

    def on_continue(self, event):
        result_frame = ResultFrame(None, title="Result Frame", f=self.f, user=self.user_id)
        result_frame.Show()
        self.Close()

    def on_new_database(self, event=None):
        new_database_name_frame = NewDatabaseNameFrame(self, title="New Database Name", f=self.f, user_id=self.user_id, new_database_frame_ref=self)
        new_database_name_frame.Show()
        self.Hide()  # Hide the current window.

    def show_result_frame(self, database_name, table_name):
        result_frame = ResultFrame(None, title="Result Frame", f=self.f, database_name=database_name, table_name=table_name)
        result_frame.Show()


class LoginFrame(wx.Frame):
    def __init__(self, parent, title, f: Firebase):
        super(LoginFrame, self).__init__(parent, title=title, size=(400, 550))

        self.f = f
        self.user = None
        self.user_id = None  # To store the user ID

        self.init_ui()
        self.Centre()
        self.Show()

    def init_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        logo = wx.StaticBitmap(panel, bitmap=wx.Bitmap("logo.png"))

        email_label = wx.StaticText(panel, label="Email", style=wx.ALIGN_CENTER, size=(200, 20))
        self.email_entry = wx.TextCtrl(panel, size=(200, 20), style=wx.TE_CENTER, value="")

        password_label = wx.StaticText(panel, label="Password", style=wx.ALIGN_CENTER, size=(200, 20))
        self.password_entry = wx.TextCtrl(panel, size=(200, 20), style=wx.TE_PASSWORD | wx.TE_CENTER, value="")

        login_button = wx.Button(panel, label="Login", size=(200, 20), style=wx.ALIGN_CENTER)
        login_button.Bind(wx.EVT_BUTTON, self.on_login)

        sizer.Add(-1, 10) 
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
        panel.SetBackgroundColour(wx.Colour(174,178,233))

    def on_login(self, event):
        email = self.email_entry.GetValue()
        password = self.password_entry.GetValue()
        try:
            self.user = self.f.login(email, password)
            self.user_id = self.user['localId']  # Get the user ID
            print("Login successful as ", self.user)
            new_database_frame = NewDatabaseFrame(None, title="New Database", f=self.f, user_id=self.user_id)
            new_database_frame.Show()
        except Exception as e:
            self.user = self.f.register(email, password)
            print("Registration successful as ", self.user)
            wx.MessageBox(f"Registration successful with '{email}'.", "Success", wx.OK | wx.ICON_INFORMATION)
            self.user = self.f.login(email, password)
            new_database_frame = NewDatabaseFrame(None, title="New Database", f=self.f, user_id=self.user_id)
            new_database_frame.Show()

        self.Close()

class ResultFrame(wx.Frame):
    def __init__(self, parent, title, f, user=None):
        super(ResultFrame, self).__init__(parent, title=title, size=(1000, 700))
        self.f = f
        self.user = user

        panel = wx.Panel(self)
        panel.SetSize(self.GetSize())  # Set the panel size to match the window size.

        sizer = wx.BoxSizer(wx.VERTICAL)

        panel_width, panel_height = panel.GetSize()

        bmp = wx.Bitmap("logo.png", wx.BITMAP_TYPE_ANY)
        logo = wx.StaticBitmap(panel, wx.ID_ANY, bmp)
        logo.SetBitmap(wx.Bitmap(wx.Image("logo.png", wx.BITMAP_TYPE_ANY).Scale(150, 150)))

        logo_height = logo.GetSize().height
        vertical_line_1 = wx.StaticLine(panel, wx.ID_ANY, style=wx.LI_VERTICAL, size=(2, logo_height))

        db_label = wx.StaticText(panel, label="DB DeskApp for PySQL", style=wx.ALIGN_CENTER)
        db_label_font = db_label.GetFont()
        db_label_font.SetPointSize(25)
        db_label_font.SetWeight(wx.FONTWEIGHT_BOLD)
        db_label.SetFont(db_label_font)
        
        vertical_line_2 = wx.StaticLine(panel, wx.ID_ANY, style=wx.LI_VERTICAL, size=(2, logo_height))

        profile_bitmap = wx.Bitmap("profile.png")
        profile_bitmap = wx.Bitmap(profile_bitmap.ConvertToImage().Scale(150, 150))
        profile_image = wx.StaticBitmap(panel, wx.ID_ANY, profile_bitmap)
        
        profile_text = wx.StaticText(panel, label="Bora Canbula", style=wx.ALIGN_CENTER)

        horizontal_line_top = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_line_top.AddSpacer(20)
        horizontal_line_top.Add(logo, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        horizontal_line_top.AddSpacer(10)
        horizontal_line_top.Add(vertical_line_1, 0, wx.ALIGN_CENTER_VERTICAL)
        horizontal_line_top.AddSpacer(120)
        horizontal_line_top.Add(db_label, 0, wx.ALIGN_CENTER_VERTICAL)
        horizontal_line_top.AddSpacer(140)
        horizontal_line_top.Add(vertical_line_2, 0, wx.ALIGN_CENTER_VERTICAL)
        horizontal_line_top.AddSpacer(10)
        horizontal_line_top.Add(profile_image, 0, wx.ALIGN_CENTER_VERTICAL)

        horizontal_line_bottom = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_line_bottom.AddSpacer(20)
        horizontal_line_bottom.AddSpacer(800)
        horizontal_line_bottom.Add(profile_text, 0, wx.ALIGN_CENTER_VERTICAL)

        button1 = wx.Button(panel, wx.ID_ANY, label="Create")
        button1.Bind(wx.EVT_BUTTON, self.to_create_table)
        button2 = wx.Button(panel, wx.ID_ANY, label="Show")
        button2.Bind(wx.EVT_BUTTON, self.on_show_databases)
        button3 = wx.Button(panel, wx.ID_ANY, label="Delete")
        button3.Bind(wx.EVT_BUTTON, self.on_delete_button_click) # Attach an event to the delete button.
        button1.SetBackgroundColour(wx.Colour(37,47,156))
        button2.SetBackgroundColour(wx.Colour(37,47,156))
        button3.SetBackgroundColour(wx.Colour(37,47,156))
        button1.SetForegroundColour(wx.WHITE)
        button2.SetForegroundColour(wx.WHITE)
        button3.SetForegroundColour(wx.WHITE)

        button_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer.AddSpacer(75)
        button_sizer.Add(button1, 0, wx.ALL, 5)
        button_sizer.AddSpacer(100)
        button_sizer.Add(button2, 0, wx.ALL, 5)
        button_sizer.AddSpacer(100)
        button_sizer.Add(button3, 0, wx.ALL, 5)

        button_container = wx.BoxSizer(wx.HORIZONTAL)
        button_container.Add(button_sizer, 0, wx.ALIGN_LEFT)

        
        horizontal_line = wx.StaticLine(panel, wx.ID_ANY, size=(panel_width, 2))
        
        sizer.Add(horizontal_line_top, 0, wx.EXPAND)
        sizer.Add(horizontal_line_bottom, 0, wx.EXPAND)
        sizer.Add(horizontal_line, 0, wx.EXPAND)
        sizer.Add(button_container, 0, wx.ALIGN_LEFT)
        
        panel.SetSizer(sizer)
        panel.SetBackgroundColour(wx.Colour(174,178,233))
        sizer.Layout()

    def to_create_table(self, event):
        create_table_frame = CreateTableFrame(None, title="Create Table", f=self.f)
        create_table_frame.Show()
        

    def on_show_databases(self, event):
        database_selection_dialog = DatabaseSelectionDialog(self, self.f)
        database_selection_dialog.ShowModal()
        database_selection_dialog.Destroy()

    def on_delete_button_click(self, event):
        delete_dialog = DeleteDialog(self, self.f)
        delete_dialog.ShowModal()
        delete_dialog.Destroy()
    

class CreateTableFrame(wx.Frame):
    def __init__(self, parent, title, f):
        super(CreateTableFrame, self).__init__(parent, title=title, size=(1000, 650))
        self.f = f

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Vertical box sizer for Table Name and Table ID
        vbox_table = wx.BoxSizer(wx.VERTICAL)
        
        # Dropdown menu for Database Name
        hbox_database_name = wx.BoxSizer(wx.HORIZONTAL)
        label_database_name = wx.StaticText(panel, label="Database Name:")
        hbox_database_name.Add(label_database_name, 0, wx.ALL | wx.CENTER, 5)
        
        # Call the Firebase function to retrieve database names.
        database_names = self.f.get_database_names()
        self.database_choice = wx.Choice(panel, choices=database_names)
        hbox_database_name.Add(self.database_choice, 0, wx.LEFT | wx.TOP, 5)
        vbox_table.Add(hbox_database_name, 0, wx.ALL | wx.EXPAND, 5)
        
        #table name
        hbox_table_name = wx.BoxSizer(wx.HORIZONTAL)
        label_table_name = wx.StaticText(panel, label="Table Name:")
        hbox_table_name.Add(label_table_name, 0, wx.ALL | wx.CENTER, 5)
        self.table_name_entry = wx.TextCtrl(panel, size=(200, -1))
        hbox_table_name.Add(self.table_name_entry, 0, wx.LEFT | wx.TOP, 5)
        vbox_table.Add(hbox_table_name, 0, wx.ALL | wx.EXPAND, 5)
        #table id
        hbox_table_id = wx.BoxSizer(wx.HORIZONTAL)
        label_table_id = wx.StaticText(panel, label="Table ID:")
        hbox_table_id.Add(label_table_id, 0, wx.ALL | wx.CENTER, 5)
        #Generate a table ID randomly.
        random_id = str(random.randint(10000, 99999))
        self.table_id_entry = wx.TextCtrl(panel, size=(100, -1), value=random_id, style=wx.TE_READONLY)
        hbox_table_id.Add(self.table_id_entry, 0, wx.LEFT | wx.TOP, 5)
        vbox_table.Add(hbox_table_id, 0, wx.ALL | wx.EXPAND, 5)


        # Save and Cancel buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(panel, label="Save")
        save_button.Bind(wx.EVT_BUTTON, self.on_save_table)
        vbox_table.Add(save_button, 0, wx.ALL | wx.EXPAND, 5)
        cancel_button = wx.Button(panel, label="Cancel")
        cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        vbox_table.Add(cancel_button, 0, wx.ALL | wx.EXPAND, 5)
        save_button.SetBackgroundColour(wx.Colour(37,47,156)) 
        cancel_button.SetBackgroundColour(wx.Colour(37,47,156)) 
        save_button.SetForegroundColour(wx.WHITE) 
        cancel_button.SetForegroundColour(wx.WHITE)

        sizer.Add(vbox_table, 0, wx.ALL | wx.EXPAND, 5)
        
        
        vbox_column = wx.BoxSizer(wx.VERTICAL)
        
        
        
        
        hbox_tables_name = wx.BoxSizer(wx.HORIZONTAL)
        label_tables_name = wx.StaticText(panel, label="Tables Name:")
        hbox_tables_name.Add(label_tables_name, 0, wx.ALL | wx.CENTER, 5)

        self.tables_choice = wx.Choice(panel)
        hbox_tables_name.Add(self.tables_choice, 0, wx.LEFT | wx.TOP, 5)
        vbox_column.Add(hbox_tables_name, 0, wx.ALL | wx.EXPAND, 5)


        

        
        # For Column Name and Data Type
        hbox_col_name = wx.BoxSizer(wx.HORIZONTAL)
        label_col_name = wx.StaticText(panel, label="Column Name:")
        hbox_col_name.Add(label_col_name, 0, wx.ALL | wx.CENTER, 5)
        self.col_name_entry = wx.TextCtrl(panel, size=(200, -1))
        hbox_col_name.Add(self.col_name_entry, 0, wx.LEFT | wx.TOP, 5)
        vbox_column.Add(hbox_col_name, 0, wx.ALL | wx.EXPAND, 5)

        hbox_type = wx.BoxSizer(wx.HORIZONTAL)
        label_type = wx.StaticText(panel, label="Data Type:")
        hbox_type.Add(label_type, 0, wx.ALL | wx.CENTER, 5)
        data_types = ['varchar', 'int', 'float', 'date']
        self.data_type_choice = wx.Choice(panel, choices=data_types)
        hbox_type.Add(self.data_type_choice, 0, wx.LEFT | wx.TOP, 5)
        vbox_column.Add(hbox_type, 0, wx.ALL | wx.EXPAND, 5)
        
        # Box sizer for Primary Key and Foreign Key
        hbox_checkboxes = wx.BoxSizer(wx.HORIZONTAL)
        self.primary_key_checkbox = wx.CheckBox(panel, label="Primary Key")
        hbox_checkboxes.Add(self.primary_key_checkbox, 0, wx.ALL | wx.LEFT, 5)
        self.foreign_key_checkbox = wx.CheckBox(panel, label="Foreign Key")
        hbox_checkboxes.Add(self.foreign_key_checkbox, 0, wx.ALL | wx.LEFT, 5)
        vbox_column.Add(hbox_checkboxes, 0, wx.ALL | wx.EXPAND, 5)

        # Create Table button
        add_button = wx.Button(panel, label="Add")
        add_button.Bind(wx.EVT_BUTTON, self.on_create_column)
        vbox_column.Add(add_button, 0, wx.ALL | wx.EXPAND, 5)
        add_button.SetBackgroundColour(wx.Colour(37,47,156))
        add_button.SetForegroundColour(wx.WHITE)

        sizer.Add(vbox_column, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(sizer)
        panel.SetBackgroundColour(wx.Colour(174,178,233))
        self.Layout()

    def on_save_table(self, event):
        database_name = self.database_choice.GetStringSelection()
        table_name = self.table_name_entry.GetValue()

        if not database_name or not table_name:
            wx.MessageBox("Database name and table name cannot be empty!", "Warning", wx.OK | wx.ICON_WARNING)
            return
        table_id = self.table_id_entry.GetValue()
        #table_id = str(random.randint(10000, 99999))  # Generate a table ID randomly

        if self.f.save_table_info(database_name, table_name, table_id):
            wx.MessageBox(f"Table '{table_name}' saved successfully in database '{database_name}'.", "Success", wx.OK | wx.ICON_INFORMATION)
            # After saving the table, update the table names.
            self.update_table_names()
        else:
            wx.MessageBox(f"Failed to save table '{table_name}' in database '{database_name}'.", "Error", wx)
            
    def update_table_names(self):
        database_name = self.database_choice.GetStringSelection()
        table_names = self.f.get_table_names(database_name)
        self.tables_choice.Clear()
        print(f"Updating table names for database '{database_name}': {table_names}")  
        if table_names:
            for table_name in table_names:
                self.tables_choice.Append(table_name)
            self.tables_choice.SetSelection(0)  # Select the first table.
        else:
            self.tables_choice.Append("No tables found")
            
    def on_cancel(self, event):
        self.Close()

    def on_create_column(self, event):
        selected_table_name = self.tables_choice.GetStringSelection()
        if not selected_table_name:
            wx.MessageBox("Please select a table name.", "Warning", wx.OK | wx.ICON_WARNING)
            return

        col_name = self.col_name_entry.GetValue()
        data_type = self.data_type_choice.GetString(self.data_type_choice.GetSelection())
        primary_key = self.primary_key_checkbox.GetValue()
        foreign_key = self.foreign_key_checkbox.GetValue()

        try:
            user = self.f.get_user()
            if user:
                user_id = user['localId']
                print(f"Creating column for user ID: {user_id}, table: {selected_table_name}")
                self.f.create_column(user_id, selected_table_name, col_name, data_type, primary_key, foreign_key)
                wx.MessageBox(f"Column '{col_name}' created successfully in table '{selected_table_name}'.", "Success", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            print(f"Error creating column: {e}")
            wx.MessageBox(f"Error creating column: {e}", "Error", wx.OK | wx.ICON_ERROR)

class DatabaseSelectionDialog(wx.Dialog):
    def __init__(self, parent, f):
        super(DatabaseSelectionDialog, self).__init__(parent, title="Select Database and Table", size=(500, 500))
        self.f = f

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Databases Choice
        hbox_database = wx.BoxSizer(wx.HORIZONTAL)
        label_database = wx.StaticText(panel, label="Databases Name:")
        hbox_database.Add(label_database, 0, wx.ALL | wx.CENTER, 5)

        self.databases_choice = wx.Choice(panel)
        hbox_database.Add(self.databases_choice, 0, wx.LEFT | wx.TOP, 5)
        sizer.Add(hbox_database, 0, wx.ALL | wx.EXPAND, 5)

        # Tables Choice
        hbox_tables_name = wx.BoxSizer(wx.HORIZONTAL)
        label_tables_name = wx.StaticText(panel, label="Tables Name:")
        hbox_tables_name.Add(label_tables_name, 0, wx.ALL | wx.CENTER, 5)

        self.tables_choice = wx.Choice(panel)
        hbox_tables_name.Add(self.tables_choice, 0, wx.LEFT | wx.TOP, 5)
        sizer.Add(hbox_tables_name, 0, wx.ALL | wx.EXPAND, 5)

        # Load Databases button
        self.load_databases_button = wx.Button(panel, label="Load Databases")
        sizer.Add(self.load_databases_button, 0, wx.ALL | wx.EXPAND, 5)
        self.load_databases_button.Bind(wx.EVT_BUTTON, self.on_load_databases)

        # Load Tables button
        self.load_tables_button = wx.Button(panel, label="Load Tables")
        sizer.Add(self.load_tables_button, 0, wx.ALL | wx.EXPAND, 5)
        self.load_tables_button.Bind(wx.EVT_BUTTON, self.on_load_tables)

        # Add Column button
        self.add_column_button = wx.Button(panel, label="Add Column")
        sizer.Add(self.add_column_button, 0, wx.ALL | wx.EXPAND, 5)
        self.add_column_button.Bind(wx.EVT_BUTTON, self.on_add_column)
        
        # Show Columns button
        self.show_columns_button = wx.Button(panel, label="Show Columns")
        sizer.Add(self.show_columns_button, 0, wx.ALL | wx.EXPAND, 5)
        self.show_columns_button.Bind(wx.EVT_BUTTON, self.on_show_columns)

        # Add Data button
        self.add_data_button = wx.Button(panel, label="Add Data")
        sizer.Add(self.add_data_button, 0, wx.ALL | wx.EXPAND, 5)
        self.add_data_button.Bind(wx.EVT_BUTTON, self.on_add_data)

        # Display Data button
        self.display_data_button = wx.Button(panel, label="Display Data")
        sizer.Add(self.display_data_button, 0, wx.ALL | wx.EXPAND, 5)
        self.display_data_button.Bind(wx.EVT_BUTTON, self.on_display_data)


        panel.SetSizer(sizer)
        panel.SetBackgroundColour(wx.Colour(174, 178, 233))

    def on_load_databases(self, event):
        user = self.f.get_user()
        if user:
            user_id = user['localId']
            database_names = self.f.get_database_names()
            self.databases_choice.Clear()
            for db_name in database_names:
                self.databases_choice.Append(db_name)
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)

    def on_load_tables(self, event):
        database_name = self.databases_choice.GetStringSelection()
        user = self.f.get_user()
        if user:
            user_id = user['localId']
            table_names = self.f.get_table_names(database_name)
            print(f"retrieved table names: {table_names}")
            self.tables_choice.Clear()
            for table_name in table_names:
                self.tables_choice.Append(table_name)
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)

    def on_show_columns(self, event):
        database_name = self.databases_choice.GetStringSelection()
        table_name = self.tables_choice.GetStringSelection()
        user = self.f.get_user()
        if user:
            user_id = user['localId']
            print(f"Showing columns for user ID: {user_id}, database: {database_name}, table: {table_name}")
            columns = self.f.get_columns(user_id, table_name)
            if columns:
                columns_frame = ColumnsFrame(self, columns)
                columns_frame.Show()
            else:
                wx.MessageBox("No columns found or unable to retrieve columns.", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)

    def on_add_data(self, event):
        database_name = self.databases_choice.GetStringSelection()
        table_name = self.tables_choice.GetStringSelection()
        user = self.f.get_user()
        if user:
            user_id = user['localId']
            # We're calling the updated get_columns method with the correct parameters.
            columns = self.f.get_columns(user_id, table_name)  # We're removing the database_name parameter.
            if columns:
                add_data_dialog = AddDataDialog(self, self.f, user_id, database_name, table_name, columns)
                add_data_dialog.ShowModal()
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)


    def on_display_data(self, event):
        database_name = self.databases_choice.GetStringSelection()
        table_name = self.tables_choice.GetStringSelection()
        user = self.f.get_user()
        if user:
            user_id = user['localId']
            data_frame = self.f.get_table_data(user_id, database_name, table_name)
            if not data_frame.empty:
                display_data_frame = DisplayDataFrame(self, data_frame)
                display_data_frame.Show()
            else:
                wx.MessageBox("No data found in the selected table.", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)
            
    def on_add_column(self, event):
        database_name = self.databases_choice.GetStringSelection()
        table_name = self.tables_choice.GetStringSelection()
        user = self.f.get_user()
        if user:
            user_id = user['localId']
            add_column_dialog = AddColumnDialog(self, self.f, user_id, database_name, table_name)
            add_column_dialog.ShowModal()
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)

class DisplayDataFrame(wx.Frame):
    def __init__(self, parent, data_frame):
        super(DisplayDataFrame, self).__init__(parent, title="Table Data", size=(600, 400))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        data_grid = wx.grid.Grid(panel)
        data_grid.CreateGrid(len(data_frame.index), len(data_frame.columns))
        
        for col_index, column in enumerate(data_frame.columns):
            data_grid.SetColLabelValue(col_index, column)
        
        for row_index, row in data_frame.iterrows():
            for col_index, value in enumerate(row):
                data_grid.SetCellValue(row_index, col_index, str(value))
        
        sizer.Add(data_grid, 1, wx.EXPAND)
        
        panel.SetSizerAndFit(sizer)
        
        self.Layout()



    def on_load_databases(self, event):
        user = self.f.get_user()
        if user:
            user_id = user['localId']
            database_names = self.f.get_database_names()
            self.databases_choice.Clear()
            for db_name in database_names:
                self.databases_choice.Append(db_name)
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)

    def on_load_tables(self, event):
        database_name = self.databases_choice.GetStringSelection()
        user = self.f.get_user()
        if user:
            user_id = user['localId']
            table_names = self.f.get_table_names(database_name)
            print(f"retrieved table names: {table_names}")
            self.tables_choice.Clear()
            for table_name in table_names:
                self.tables_choice.Append(table_name)
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)

    def on_show_columns(self, event):
        database_name = self.databases_choice.GetStringSelection()
        table_name = self.tables_choice.GetStringSelection()
        if database_name and table_name:  # Check the database and table names.
            user = self.f.get_user()
            if user:
                user_id = user['localId']
                columns = self.f.get_columns(user_id, database_name, table_name)
                if columns:
                    columns_frame = ColumnsFrame(self, columns)
                    columns_frame.Show()
                else:
                    wx.MessageBox("No columns found for the selected table.", "Info", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Please select a database and a table first.", "Error", wx.OK | wx.ICON_ERROR)
            
class DeleteDialog(wx.Dialog):
    def __init__(self, parent, f):
        super(DeleteDialog, self).__init__(parent, title="Delete Database or Table", size=(400, 300))
        self.f = f

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Databases Choice
        hbox_database = wx.BoxSizer(wx.HORIZONTAL)
        label_database = wx.StaticText(panel, label="Database Name:")
        hbox_database.Add(label_database, 0, wx.ALL | wx.CENTER, 5)

        self.databases_choice = wx.Choice(panel)
        hbox_database.Add(self.databases_choice, 0, wx.LEFT | wx.TOP, 5)
        sizer.Add(hbox_database, 0, wx.ALL | wx.EXPAND, 5)

        # Tables Choice
        hbox_tables_name = wx.BoxSizer(wx.HORIZONTAL)
        label_tables_name = wx.StaticText(panel, label="Table Name:")
        hbox_tables_name.Add(label_tables_name, 0, wx.ALL | wx.CENTER, 5)

        self.tables_choice = wx.Choice(panel)
        hbox_tables_name.Add(self.tables_choice, 0, wx.LEFT | wx.TOP, 5)
        sizer.Add(hbox_tables_name, 0, wx.ALL | wx.EXPAND, 5)

         # Columns Choice
        hbox_columns_name = wx.BoxSizer(wx.HORIZONTAL)
        label_columns_name = wx.StaticText(panel, label="Column Name:")
        hbox_columns_name.Add(label_columns_name, 0, wx.ALL | wx.CENTER, 5)

        self.columns_choice = wx.Choice(panel)
        hbox_columns_name.Add(self.columns_choice, 0, wx.LEFT | wx.TOP, 5)
        sizer.Add(hbox_columns_name, 0, wx.ALL | wx.EXPAND, 5)


        # Delete Database button
        self.delete_database_button = wx.Button(panel, label="Delete Database")
        sizer.Add(self.delete_database_button, 0, wx.ALL | wx.EXPAND, 5)
        self.delete_database_button.Bind(wx.EVT_BUTTON, self.on_delete_database)

        # Delete Table button
        self.delete_table_button = wx.Button(panel, label="Delete Table")
        sizer.Add(self.delete_table_button, 0, wx.ALL | wx.EXPAND, 5)
        self.delete_table_button.Bind(wx.EVT_BUTTON, self.on_delete_table)

        # Delete Column button
        self.delete_column_button = wx.Button(panel, label="Delete Column")
        sizer.Add(self.delete_column_button, 0, wx.ALL | wx.EXPAND, 5)
        self.delete_column_button.Bind(wx.EVT_BUTTON, self.on_delete_column)

        panel.SetSizer(sizer)
        panel.SetBackgroundColour(wx.Colour(255, 182, 193))

        self.load_databases()

    def load_databases(self):
        user = self.f.get_user()
        if user:
            user_uid = user['localId']
            database_names = self.f.get_database_names()
            self.databases_choice.Clear()
            for db_name in database_names:
                self.databases_choice.Append(db_name)
            self.databases_choice.Bind(wx.EVT_CHOICE, self.on_database_selected)
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)

    def on_database_selected(self, event):
        self.load_tables()

    def load_tables(self):
        database_name = self.databases_choice.GetStringSelection()
        if database_name:
            table_names = self.f.get_table_names(database_name)
            self.tables_choice.Clear()
            for table_name in table_names:
                self.tables_choice.Append(table_name)
            self.tables_choice.Bind(wx.EVT_CHOICE, self.on_table_selected)
    
    def on_table_selected(self, event):
        self.load_columns()
    
    def load_columns(self):
        user = self.f.get_user()
        if user:
            user_uid = user['localId']
            database_name = self.databases_choice.GetStringSelection()
            table_name = self.tables_choice.GetStringSelection()
            if database_name and table_name:
                column_names = self.f.get_columns(user_uid, table_name)
                self.columns_choice.Clear()
                for column in column_names:
                    self.columns_choice.Append(column['name'])
        else:
            wx.MessageBox("User is not authenticated.", "Error", wx.OK | wx.ICON_ERROR)
    def on_delete_database(self, event):
        database_name = self.databases_choice.GetStringSelection()
        if not database_name:
            wx.MessageBox("Please select a database.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        confirm_dialog = wx.MessageDialog(self, f"Are you sure you want to delete the database '{database_name}'?",
                                          "Confirm Deletion", wx.YES_NO | wx.ICON_QUESTION)
        result = confirm_dialog.ShowModal()
        
        if result == wx.ID_YES:
            user = self.f.get_user()
            if user:
                user_uid = user['localId']
                self.f.delete_database(user_uid, database_name)
                wx.MessageBox(f"Database '{database_name}' deleted successfully.", "Info", wx.OK | wx.ICON_INFORMATION)
                self.load_databases()
                self.tables_choice.Clear()
                self.columns_choice.Clear()
        confirm_dialog.Destroy()

    def on_delete_table(self, event):
        database_name = self.databases_choice.GetStringSelection()
        table_name = self.tables_choice.GetStringSelection()
        if not database_name or not table_name:
            wx.MessageBox("Please select both a database and a table.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        confirm_dialog = wx.MessageDialog(self, f"Are you sure you want to delete the table '{table_name}' in database '{database_name}'?",
                                          "Confirm Deletion", wx.YES_NO | wx.ICON_QUESTION)
        result = confirm_dialog.ShowModal()
        
        if result == wx.ID_YES:
            user = self.f.get_user()
            if user:
                user_uid = user['localId']
                self.f.delete_table(user_uid, database_name, table_name)
                wx.MessageBox(f"Table '{table_name}' in database '{database_name}' deleted successfully.", "Info", wx.OK | wx.ICON_INFORMATION)
                self.load_tables()
                self.columns_choice.Clear()
        confirm_dialog.Destroy()
    
    def on_delete_column(self, event):
        database_name = self.databases_choice.GetStringSelection()
        table_name = self.tables_choice.GetStringSelection()
        column_name = self.columns_choice.GetStringSelection()
        if not database_name or not table_name or not column_name:
            wx.MessageBox("Please select a database, table, and column.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        confirm_dialog = wx.MessageDialog(self, f"Are you sure you want to delete the column '{column_name}' in table '{table_name}' of database '{database_name}'?",
                                          "Confirm Deletion", wx.YES_NO | wx.ICON_QUESTION)
        result = confirm_dialog.ShowModal()

        if result == wx.ID_YES:
            user = self.f.get_user()
            if user:
                user_uid = user['localId']
                self.f.delete_column(user_uid, database_name, table_name, column_name)
                wx.MessageBox(f"Column '{column_name}' in table '{table_name}' of database '{database_name}' deleted successfully.", "Info", wx.OK | wx.ICON_INFORMATION)
                self.load_columns()
        confirm_dialog.Destroy()

class ColumnsFrame(wx.Frame):
    def __init__(self, parent, columns):
        super(ColumnsFrame, self).__init__(parent, title="Table Columns", size=(400, 300))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        columns_grid = wx.GridSizer(rows=len(columns) + 1, cols=4, hgap=5, vgap=5)
        
        headers = ["Column Name", "Data Type", "Primary Key", "Foreign Key"]
        for header in headers:
            columns_grid.Add(wx.StaticText(panel, label=header), 0, wx.EXPAND)
        
        for column in columns:
            columns_grid.Add(wx.StaticText(panel, label=column["name"]), 0, wx.EXPAND)
            columns_grid.Add(wx.StaticText(panel, label=column["data_type"]), 0, wx.EXPAND)
            columns_grid.Add(wx.StaticText(panel, label=str(column["primary_key"])), 0, wx.EXPAND)
            columns_grid.Add(wx.StaticText(panel, label=str(column["foreign_key"])), 0, wx.EXPAND)
        
        sizer.Add(columns_grid, 1, wx.ALL | wx.EXPAND, 5)
        
        panel.SetSizerAndFit(sizer)
        
        self.Layout()
        
class AddDataDialog(wx.Dialog):
    def __init__(self, parent, f, user_id, database_name, table_name, columns):
        super(AddDataDialog, self).__init__(parent, title="Add Data to Table", size=(400, 300))
        self.f = f
        self.user_id = user_id
        self.database_name = database_name
        self.table_name = table_name
        self.columns = columns

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.data_entries = {}
        for column in columns:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(panel, label=f"{column['name']}:")
            hbox.Add(label, 0, wx.ALL | wx.CENTER, 5)

            entry = wx.TextCtrl(panel)
            self.data_entries[column['name']] = entry
            hbox.Add(entry, 0, wx.ALL | wx.CENTER, 5)

            sizer.Add(hbox, 0, wx.ALL | wx.EXPAND, 5)

        self.save_button = wx.Button(panel, label="Save")
        sizer.Add(self.save_button, 0, wx.ALL | wx.CENTER, 5)
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        panel.SetSizer(sizer)

    def on_save(self, event):
        data = {col['name']: self.data_entries[col['name']].GetValue() for col in self.columns}
        self.f.add_data_to_table(self.user_id, self.database_name, self.table_name, data)
        wx.MessageBox("Data added successfully.", "Info", wx.OK | wx.ICON_INFORMATION)
        self.Close()

class AddColumnDialog(wx.Dialog):
    def __init__(self, parent, f, user_id, database_name, table_name):
        super(AddColumnDialog, self).__init__(parent, title="Add Column", size=(400, 300))
        self.f = f
        self.user_id = user_id
        self.database_name = database_name
        self.table_name = table_name

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Column Name
        hbox_col_name = wx.BoxSizer(wx.HORIZONTAL)
        label_col_name = wx.StaticText(panel, label="Column Name:")
        hbox_col_name.Add(label_col_name, 0, wx.ALL | wx.CENTER, 5)

        self.col_name_entry = wx.TextCtrl(panel)
        hbox_col_name.Add(self.col_name_entry, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(hbox_col_name, 0, wx.ALL | wx.EXPAND, 5)

        # Data Type
        hbox_data_type = wx.BoxSizer(wx.HORIZONTAL)
        label_data_type = wx.StaticText(panel, label="Data Type:")
        hbox_data_type.Add(label_data_type, 0, wx.ALL | wx.CENTER, 5)

        self.data_type_choice = wx.Choice(panel, choices=['varchar', 'int', 'float', 'date'])
        hbox_data_type.Add(self.data_type_choice, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(hbox_data_type, 0, wx.ALL | wx.EXPAND, 5)

        # Primary Key Checkbox
        hbox_primary_key = wx.BoxSizer(wx.HORIZONTAL)
        label_primary_key = wx.StaticText(panel, label="Primary Key:")
        hbox_primary_key.Add(label_primary_key, 0, wx.ALL | wx.CENTER, 5)

        self.primary_key_checkbox = wx.CheckBox(panel)
        hbox_primary_key.Add(self.primary_key_checkbox, 1, wx.ALL | wx.CENTER, 5)
        sizer.Add(hbox_primary_key, 0, wx.ALL | wx.EXPAND, 5)

        # Foreign Key Checkbox
        hbox_foreign_key = wx.BoxSizer(wx.HORIZONTAL)
        label_foreign_key = wx.StaticText(panel, label="Foreign Key:")
        hbox_foreign_key.Add(label_foreign_key, 0, wx.ALL | wx.CENTER, 5)

        self.foreign_key_checkbox = wx.CheckBox(panel)
        hbox_foreign_key.Add(self.foreign_key_checkbox, 1, wx.ALL | wx.CENTER, 5)
        sizer.Add(hbox_foreign_key, 0, wx.ALL | wx.EXPAND, 5)

        # Add Column Button
        self.add_column_button = wx.Button(panel, label="Add Column")
        self.add_column_button.Bind(wx.EVT_BUTTON, self.on_add_column)
        sizer.Add(self.add_column_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)

    def on_add_column(self, event):
        col_name = self.col_name_entry.GetValue()
        data_type = self.data_type_choice.GetString(self.data_type_choice.GetSelection())
        primary_key = self.primary_key_checkbox.GetValue()
        foreign_key = self.foreign_key_checkbox.GetValue()

        try:
            self.f.create_column(self.user_id, self.table_name, col_name, data_type, primary_key, foreign_key)
            wx.MessageBox(f"Column '{col_name}' created successfully in table '{self.table_name}'.", "Success", wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except Exception as e:
            wx.MessageBox(f"Error creating column: {e}", "Error", wx.OK | wx.ICON_ERROR)


if __name__ == "__main__":
    app = wx.App()
    f = Firebase()
    login_frame = LoginFrame(None, title="Login to DeskApp", f=f)
    app.MainLoop()