import wx
import wx.grid
import wx.lib.mixins.inspection as wit
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from db import Database
import json




class MainFrame(wx.Frame):
    
    BG_COLOR = wx.Colour(223, 232, 232) 
    TEXT_COLOR = wx.Colour(0, 0, 0)  # Black text color
    MENU_BG_COLOR = wx.Colour(207, 231, 252)  # Menu background color
    MENU_TEXT_COLOR = wx.Colour(0, 0, 0)  # Menu text color
    
    
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.db = Database()
        self.db.create_database("path_to_your_database.db")
        self.table_choices = None

        #icon = wx.Icon("icon.png", wx.BITMAP_TYPE_ICO)
        #self.SetIcon(icon)

        # Create a menu bar
        menubar = wx.MenuBar()
        #menubar.SetBackgroundColour(self.MENU_BG_COLOR)

        # File menu
        file_menu = wx.Menu()
        
        create_database = file_menu.Append(wx.ID_ANY, '&Create', 'Create database')
        open_item = file_menu.Append(wx.ID_OPEN, '&Open', 'Open a new document')
        save_item = file_menu.Append(wx.ID_SAVE, '&Save', 'Save the current document')
        exportTxt = file_menu.Append(wx.ID_ANY, 'Export as Text', 'Export table as text file')
        exportCsv = file_menu.Append(wx.ID_ANY, 'Export as CSV', 'Export table as CSV file')
        exportJson = file_menu.Append(wx.ID_ANY, 'Export as Json', 'Export as Json file')
        importTxt = file_menu.Append(wx.ID_ANY, 'Import Text', 'Import table from text file')
        importCsv = file_menu.Append(wx.ID_ANY, 'Import CSV', 'Import table from CSV file')

        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, '&Exit', 'Exit application')
        menubar.Append(file_menu, '&File')

        self.Bind(wx.EVT_MENU, self.on_export_text, exportTxt)
        self.Bind(wx.EVT_MENU, self.on_export_csv, exportCsv)
        self.Bind(wx.EVT_MENU, self.on_export_json, exportJson)
        self.Bind(wx.EVT_MENU, self.on_import_text, importTxt)
        self.Bind(wx.EVT_MENU, self.on_import_csv, importCsv)

        self.SetSize((600, 400))
        self.SetTitle('Database Export/Import Example')
        self.Centre()

        # Edit menu
        edit_menu = wx.Menu()
        copy_item = edit_menu.Append(wx.ID_COPY, '&Copy', 'Copy text')
        paste_item = edit_menu.Append(wx.ID_PASTE, '&Paste', 'Paste text')
        menubar.Append(edit_menu, '&Edit')

        # View menu
        view_menu = wx.Menu()
        zoom_in_item = view_menu.Append(wx.ID_ZOOM_IN, 'Zoom &In', 'Zoom in')
        zoom_out_item = view_menu.Append(wx.ID_ZOOM_OUT, 'Zoom &Out', 'Zoom out')
        menubar.Append(view_menu, '&View')

        # Set the menu bar
        self.SetMenuBar(menubar)

        # Bind menu events
        self.Bind(wx.EVT_MENU, self.on_create_database, create_database)
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_copy, copy_item)
        self.Bind(wx.EVT_MENU, self.on_paste, paste_item)
        self.Bind(wx.EVT_MENU, self.on_zoom_in, zoom_in_item)
        self.Bind(wx.EVT_MENU, self.on_zoom_out, zoom_out_item)

        # Set up the main panel and sizer
        panel = wx.Panel(self)
        panel.SetBackgroundColour(self.BG_COLOR)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Database file selection
        self.db_file_picker = wx.FilePickerCtrl(panel, message="Select a database file", wildcard="*.db")
        vbox.Add(self.db_file_picker, flag=wx.EXPAND | wx.ALL, border=10)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_select_db_file, self.db_file_picker)

        # Table selection
        self.table_choice = wx.Choice(panel)
        #self.table_choice.SetBackgroundColour(self.BG_COLOR)
        vbox.Add(self.table_choice, flag=wx.EXPAND | wx.ALL, border=10)
        self.update_table_choices()

        # Notebook for different functionalities
        self.notebook = wx.Notebook(panel)
        #self.notebook.SetBackgroundColour(self.BG_COLOR)
        vbox.Add(self.notebook, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Pages
        self.query_page = QueryPage(self.notebook, self.db)
        self.create_table_page = CreateTablePage(self.notebook, self.db)
        self.view_table_page = ViewTablePage(self.notebook, self.db ,self.table_choice )
        #self.graph_page = GraphPage(self.notebook, self.db, self.table_choice)

        self.notebook.AddPage(self.query_page, "Execute Query")
        self.notebook.AddPage(self.create_table_page, "Create Table")
        self.notebook.AddPage(self.view_table_page, "View Table")
        #self.notebook.AddPage(self.graph_page, "Graph Data")

        panel.SetSizer(vbox)

        self.SetTitle("DBmatik")
        self.SetSize((800, 600))
        self.Centre()

    
    def on_export_json(self, event):
        selected_table = self.table_choice.GetStringSelection()
        if not selected_table:
            wx.MessageBox("No table selected", "Error", wx.OK | wx.ICON_ERROR)
            return
        with wx.FileDialog(self, "Save JSON file", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            self.db.export_table_to_json(selected_table, pathname)
    
    
    def on_create_database(self, event):
        dialog = CreateDatabaseDialog(self)
        
        if dialog.ShowModal() == wx.ID_OK:
            try:
                self.db.create_database(dialog.get_input())
                wx.MessageBox("Database created successfully.", "Info", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()
            

    
    
    
    def update_table_choices(self):
        tables = self.db.get_tables()  
        self.table_choice.Set(tables)
        if tables:
            self.table_choice.SetSelection(0)

    def on_open(self, event):
        with wx.FileDialog(self, "Open DB file", wildcard="Database files (*.db)|*.db",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            path = fileDialog.GetPath()
            self.db.create_database(path)
            self.update_table_choices()
            wx.MessageBox(f"Connected to {path}", "Info", wx.OK | wx.ICON_INFORMATION)
            print(f"Connected to database at {path}")

    def on_save(self, event):
        with wx.FileDialog(self, "Save DB file", wildcard="Database files (*.db)|*.db",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            path = fileDialog.GetPath()
            self.db.create_database(path)
            wx.MessageBox(f"Database saved at {path}", "Info", wx.OK | wx.ICON_INFORMATION)
            print(f"Database saved at {path}")

    def on_export_text(self, event):
        selected_table = self.table_choice.GetStringSelection()
        if not selected_table:
            wx.MessageBox("No table selected", "Error", wx.OK | wx.ICON_ERROR)
            return
        with wx.FileDialog(self, "Save text file", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            self.db.export_table_to_text(selected_table, pathname)

    def on_export_csv(self, event):
        selected_table = self.table_choice.GetStringSelection()
        if not selected_table:
            wx.MessageBox("No table selected", "Error", wx.OK | wx.ICON_ERROR)
            return
        with wx.FileDialog(self, "Save CSV file", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            self.db.export_table_to_csv(selected_table, pathname)

    def on_import_text(self, event):
        selected_table = self.table_choice.GetStringSelection()
        if not selected_table:
            wx.MessageBox("No table selected", "Error", wx.OK | wx.ICON_ERROR)
            return
        with wx.FileDialog(self, "Open text file", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            self.db.import_table_from_text(selected_table, pathname)

    def on_import_csv(self, event):
        selected_table = self.table_choice.GetStringSelection()
        if not selected_table:
            wx.MessageBox("No table selected", "Error", wx.OK | wx.ICON_ERROR)
            return
        with wx.FileDialog(self, "Open CSV file", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            self.db.import_table_from_csv(selected_table, pathname)

    def on_exit(self, event):
        self.db.close_connection()
        self.Close(True)

    def on_copy(self, event):
        print("Copy selected")

    def on_paste(self, event):
        print("Paste selected")

    def on_zoom_in(self, event):
        print("Zoom in selected")

    def on_zoom_out(self, event):
        print("Zoom out selected")

    def on_select_db_file(self, event):
        db_file_path = self.db_file_picker.GetPath()
        self.db.create_database(db_file_path)
        self.update_table_choices()
        wx.MessageBox(f"Connected to {db_file_path}", "Info", wx.OK | wx.ICON_INFORMATION)
        print(f"Connected to database at {db_file_path}")

    def on_close(self, event):
        self.db.close_connection()
        self.Destroy()



class QueryPage(wx.Panel):
    def __init__(self, parent, db):
        super(QueryPage, self).__init__(parent)

        self.db = db

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Text control for SQL query input
        self.query_input = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        vbox.Add(self.query_input, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)

        # Execute query button
        execute_button = wx.Button(self, label="Execute Query")
        vbox.Add(execute_button, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        self.Bind(wx.EVT_BUTTON, self.on_execute_query, execute_button)

        # Grid for query output
        self.query_grid = wx.grid.Grid(self)
        self.query_grid.CreateGrid(0, 0)  # Initially create an empty grid
        vbox.Add(self.query_grid, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)

        self.SetSizer(vbox)

    def on_execute_query(self, event):
        query = self.query_input.GetValue()
        try:
            column_names, result = self.db.execute_query(query)
            self.display_query_result(column_names, result)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

    def display_query_result(self, column_names, result):
        num_rows = len(result)
        num_cols = len(column_names)

        self.query_grid.ClearGrid()

        # Ensure the grid has enough rows and columns
        current_rows = self.query_grid.GetNumberRows()
        current_cols = self.query_grid.GetNumberCols()

        if current_rows < num_rows:
            self.query_grid.AppendRows(num_rows - current_rows)
        elif current_rows > num_rows:
            self.query_grid.DeleteRows(num_rows, current_rows - num_rows)

        if current_cols < num_cols:
            self.query_grid.AppendCols(num_cols - current_cols)
        elif current_cols > num_cols:
            self.query_grid.DeleteCols(num_cols, current_cols - num_cols)

        # Set column labels
        for i, col_name in enumerate(column_names):
            self.query_grid.SetColLabelValue(i, str(col_name))

        # Populate grid with data
        for i, row in enumerate(result):
            for j, value in enumerate(row):
                self.query_grid.SetCellValue(i, j, str(value))

        # Refresh the grid to ensure changes are displayed
        self.query_grid.ForceRefresh()


class CreateTablePage(wx.Panel):
    def __init__(self, parent, db):
        super(CreateTablePage, self).__init__(parent)

        self.db = db

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Table name input
        hbox_table = wx.BoxSizer(wx.HORIZONTAL)
        table_name_label = wx.StaticText(self, label="Table Name:")
        hbox_table.Add(table_name_label, flag=wx.RIGHT, border=8)
        self.table_name_input = wx.TextCtrl(self)
        hbox_table.Add(self.table_name_input, proportion=1)
        vbox.Add(hbox_table, flag=wx.EXPAND|wx.ALL, border=10)

        # Columns input
        hbox_columns = wx.BoxSizer(wx.HORIZONTAL)
        columns_label = wx.StaticText(self, label="Columns (name type, ...):")
        hbox_columns.Add(columns_label, flag=wx.RIGHT, border=8)
        self.columns_input = wx.TextCtrl(self)
        hbox_columns.Add(self.columns_input, proportion=1)
        vbox.Add(hbox_columns, flag=wx.EXPAND|wx.ALL, border=10)

        # Primary key input
        hbox_pk = wx.BoxSizer(wx.HORIZONTAL)
        pk_label = wx.StaticText(self, label="Primary Key (optional):")
        hbox_pk.Add(pk_label, flag=wx.RIGHT, border=8)
        self.pk_input = wx.TextCtrl(self)
        hbox_pk.Add(self.pk_input, proportion=1)
        vbox.Add(hbox_pk, flag=wx.EXPAND|wx.ALL, border=10)

        # Create table button
        create_button = wx.Button(self, label="Create Table")
        vbox.Add(create_button, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        self.Bind(wx.EVT_BUTTON, self.on_create_table, create_button)

        self.SetSizer(vbox)

    def on_create_table(self, event):
        table_name = self.table_name_input.GetValue()
        columns_input = self.columns_input.GetValue()

        # Split columns and trim any extra spaces
        columns = [col.strip().split(" ") for col in columns_input.split(",")]
        columns = [(col[0], col[1]) for col in columns if len(col) == 2]

        primary_key = self.pk_input.GetValue() or None

        try:
            self.db.create_table(table_name, columns, primary_key)
            wx.MessageBox(f"Table {table_name} created successfully", "Info", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)



class ViewTablePage(wx.Panel):
    def __init__(self, parent, db , table_choice):
        super(ViewTablePage, self).__init__(parent)

        self.db = db
        
        self.original_data = []
        self.table_choice = table_choice

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Vertical box sizer for buttons and input controls
        vbox_controls = wx.BoxSizer(wx.VERTICAL)

        hbox_table = wx.BoxSizer(wx.HORIZONTAL)
        table_name_label = wx.StaticText(self, label="Table Name:")
        hbox_table.Add(table_name_label, flag=wx.RIGHT, border=8)
        self.table_name_input = wx.TextCtrl(self)
        hbox_table.Add(self.table_name_input, proportion=1)
        vbox_controls.Add(hbox_table, flag=wx.EXPAND | wx.ALL, border=10)

        # Add a table selector
        #hbox_selector = wx.BoxSizer(wx.HORIZONTAL)
        #table_selector_label = wx.StaticText(self, label="Select a table:")
        #hbox_selector.Add(table_selector_label, flag=wx.RIGHT, border=8)

        # Fetch table names from the database
        #table_names = self.db.get_tables()
        #print(f"Table names fetched from the database: {table_names}")  # Debug statement
        #self.table_selector = wx.Choice(self, choices=table_names)
        #hbox_selector.Add(self.table_selector, proportion=1)
        #vbox_controls.Add(hbox_selector, flag=wx.EXPAND | wx.ALL, border=10)

        
        view_button = wx.Button(self, label="View Table")
        vbox_controls.Add(view_button, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.on_view_table, view_button)


        
        insert_button = wx.Button(self, label="Insert Data")
        vbox_controls.Add(insert_button, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.on_insert_data, insert_button)

        delete_button = wx.Button(self, label="Delete Data")
        vbox_controls.Add(delete_button, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.on_delete_data, delete_button)

        add_column = wx.Button(self, label="Add Column")
        vbox_controls.Add(add_column, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.on_add_column, add_column)

        delete_column = wx.Button(self, label="Delete Column")
        vbox_controls.Add(delete_column, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.on_delete_column, delete_column)

        update_button = wx.Button(self, label="Save Table")
        vbox_controls.Add(update_button, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.on_update_data, update_button)

        delete_table_button = wx.Button(self, label="Delete Table")
        vbox_controls.Add(delete_table_button, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.on_delete_table, delete_table_button)
        
        main_sizer.Add(vbox_controls, flag=wx.EXPAND | wx.ALL, border=10)

        # Grid for query output
        self.query_grid = wx.grid.Grid(self)
        self.query_grid.CreateGrid(0, 0)
        main_sizer.Add(self.query_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(main_sizer)

    
    def on_delete_table(self , event):
        selected_table = self.table_choice.GetStringSelection()
        
        if not selected_table:
            wx.MessageBox("Please select a table", "Error", wx.OK | wx.ICON_ERROR)
            return
        dialog = DeleteTableDialog(self, selected_table)
        dialog.ShowModal()
        


    
    def on_view_table(self, event):
        selected_table = self.table_choice.GetStringSelection()
        if not selected_table:
            wx.MessageBox("Please select a table", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            column_names, result = self.db.execute_query(f"SELECT * FROM {selected_table}")
            if column_names is None or result is None:
                raise Exception("Failed to fetch data from the table")
            self.display_query_result(column_names, result)
            self.original_data = result  # Store the original data
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


    def display_query_result(self, column_names, result):
        num_rows = len(result)
        num_cols = len(column_names)

        self.query_grid.ClearGrid()

        # Ensure the grid has enough rows and columns
        current_rows = self.query_grid.GetNumberRows()
        current_cols = self.query_grid.GetNumberCols()

        if current_rows < num_rows:
            self.query_grid.AppendRows(num_rows - current_rows)
        elif current_rows > num_rows:
            self.query_grid.DeleteRows(num_rows, current_rows - num_rows)

        if current_cols < num_cols:
            self.query_grid.AppendCols(num_cols - current_cols)
        elif current_cols > num_cols:
            self.query_grid.DeleteCols(num_cols, current_cols - num_cols)

        # Set column labels
        for i, col_name in enumerate(column_names):
            self.query_grid.SetColLabelValue(i, str(col_name))

        # Populate grid with data
        for i, row in enumerate(result):
            for j, value in enumerate(row):
                self.query_grid.SetCellValue(i, j, str(value))

        # Refresh the grid to ensure changes are displayed
        self.query_grid.ForceRefresh()


    def on_update_data(self , event):
        updated_data = []
        
        for i in range(self.query_grid.GetNumberRows()):
            row = {}
            for n in range(self.query_grid.GetNumberCols()):
                column_names = self.query_grid.GetColLabelValue(n)
                cell_value = str(self.query_grid.GetCellValue(i,n))
                if cell_value.isdigit():

                    cell_value = int(cell_value)
                    
                row[column_names] = cell_value
                  
            updated_data.append(row)


          
        unique_column_name = self.db.get_columns_of_table(self.table_choice.GetStringSelection())
        self.db.update_data((self.table_choice.GetStringSelection()), updated_data, unique_column_name)
        print("aaaaa")
                
        


    def on_insert_data(self, event):
        selected_table = self.table_choice.GetStringSelection()
        if not selected_table:
            wx.MessageBox("Please select a table", "Error", wx.OK | wx.ICON_ERROR)
            return

        columns_info = self.db.get_columns_of_table(selected_table)
        if columns_info is None:
            wx.MessageBox("No column information available for the selected table", "Error", wx.OK | wx.ICON_ERROR)
            return

        dialog = InsertDataDialog(self, selected_table, columns_info)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.get_data()
            try:
                self.db.insert_data(selected_table, data)
                wx.MessageBox("Data inserted successfully", "Info", wx.OK | wx.ICON_INFORMATION)
                self.on_view_table(None)  # Refresh the table view after inserting data
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

        dialog.Destroy()

    def on_delete_data(self, event):
        selected_table = self.table_choice.GetStringSelection()
        data_list = []
        columns = None
        for i in range(self.query_grid.GetNumberRows()):
            row = {}
            for n in range(self.query_grid.GetNumberCols()):
                column_name = self.query_grid.GetColLabelValue(n)
                cell_value = str(self.query_grid.GetCellValue(i, n))
                if cell_value.isdigit():
                    cell_value = int(cell_value)

                row[column_name] = cell_value
            data_list.append(row)

        # Get columns from the first row
        if data_list:
            columns = data_list[0].keys()

        if not selected_table:
            wx.MessageBox("Please select a table", "Error", wx.OK | wx.ICON_ERROR)
            return

        if columns is None:
            wx.MessageBox("No column information available for the selected table", "Error", wx.OK | wx.ICON_ERROR)
            return

        dialog = DeleteDataDialog(self, selected_table, columns)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.get_data()
            try:
                self.db.delete_data(selected_table, data)
                wx.MessageBox("Data deleted successfully", "Info", wx.OK | wx.ICON_INFORMATION)
                self.on_view_table(None)
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

        dialog.Destroy()

    def on_add_column(self, event):
        selected_table = self.table_choice.GetStringSelection()
        dialog = AddColumnDialog(self, selected_table)
        if dialog.ShowModal() == wx.ID_OK:
            column_name, data_type = dialog.get_column_data()
            query = f"ALTER TABLE {selected_table} ADD COLUMN {column_name} {data_type}"
            print(query)
            try:
                self.db.cursor.execute(query)
                wx.MessageBox("Column added successfully", "Info", wx.OK | wx.ICON_INFORMATION)
                self.on_view_table(None)
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


    def on_delete_column(self, event):
        selected_table = self.table_choice.GetStringSelection()
        dialog = DeleteColumnDialog(self, selected_table)
        if dialog.ShowModal() == wx.ID_OK:
            column_name = dialog.get_column_data()
            temp_table = f"{selected_table}_temp"
            
            try:
                # Step 1: Get existing columns except the one to be deleted
                cursor = self.db.cursor
                cursor.execute(f"PRAGMA table_info({selected_table})")
                columns = [info[1] for info in cursor.fetchall() if info[1] != column_name]
                columns_str = ", ".join(columns)

                # Step 2: Create a new table without the column to be deleted
                cursor.execute(f"CREATE TABLE {temp_table} AS SELECT {columns_str} FROM {selected_table}")

                # Step 3: Drop the old table
                cursor.execute(f"DROP TABLE {selected_table}")

                # Step 4: Rename the new table to the old table's name
                cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {selected_table}")

                wx.MessageBox("Column deleted successfully", "Info", wx.OK | wx.ICON_INFORMATION)
                self.on_view_table(None)
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

class DeleteTableDialog(wx.Dialog):
    def __init__(self, parent, table_name):
        super(DeleteTableDialog, self).__init__(parent, title=f"Delete Table: {table_name}")

        self.table_name = table_name
        
        self.data = {}

        # Create a panel
        panel = wx.Panel(self)

        # Use a box sizer for layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label=f"Are you sure you want to delete {table_name}")
        hbox.Add(label, proportion=1, flag=wx.RIGHT, border=8)

        # Add buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_delete = wx.Button(panel, label="Delete")
        btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        
        hbox_buttons.Add(btn_delete, flag=wx.ALIGN_BOTTOM, border=8)
        btn_cancel = wx.Button(panel, label="Cancel")
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox_buttons.Add(btn_cancel, flag=wx.ALIGN_BOTTOM, border=8)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.SetInitialSize((400, 300))
        self.Fit()

    def on_delete(self, event):
        self.GetParent().db.delete_table(self.table_name)
        self.Destroy()


    def on_cancel(self, event):
        self.Destroy()



class AddColumnDialog(wx.Dialog):
    def __init__(self, parent, table_name):
        super(AddColumnDialog, self).__init__(parent, title=f"Add Column for {table_name}")

        self.table_name = table_name
        self.column_name = ""
        self.data_type = ""

        # Create a panel
        panel = wx.Panel(self)

        # Use a box sizer for layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create text controls for each column
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, label=f"Column Name:")
        hbox.Add(label, proportion=1, flag=wx.RIGHT, border=8)
        self.text_ctrl = wx.TextCtrl(panel)
        hbox.Add(self.text_ctrl, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND|wx.ALL, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, label=f"Data Type:")
        hbox.Add(label, proportion=1, flag=wx.RIGHT, border=8)
        self.text_ctrl_2 = wx.TextCtrl(panel)
        hbox.Add(self.text_ctrl_2, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND|wx.ALL, border=10)

        # Add buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, label="Add Column")
        btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        hbox_buttons.Add(btn_ok, flag=wx.RIGHT, border=8)
        btn_cancel = wx.Button(panel, label="Cancel")
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox_buttons.Add(btn_cancel, flag=wx.RIGHT, border=8)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.SetInitialSize((400, 300))
        self.Fit()

    def on_ok(self, event):
        self.column_name = self.text_ctrl.GetValue()
        self.data_type = self.text_ctrl_2.GetValue()
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def get_column_data(self):
        return self.column_name, self.data_type



class DeleteColumnDialog(wx.Dialog):
    def __init__(self, parent, table_name):
        super(DeleteColumnDialog, self).__init__(parent, title=f"Delete Column from {table_name}")

        self.table_name = table_name
        self.column_name = ""

        # Create a panel
        panel = wx.Panel(self)

        # Use a box sizer for layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create text controls for column name
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, label="Column Name:")
        hbox.Add(label, proportion=1, flag=wx.RIGHT, border=8)
        self.text_ctrl = wx.TextCtrl(panel)
        hbox.Add(self.text_ctrl, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=10)

        # Add buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, label="Delete Column")
        btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        hbox_buttons.Add(btn_ok, flag=wx.RIGHT, border=8)
        btn_cancel = wx.Button(panel, label="Cancel")
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox_buttons.Add(btn_cancel, flag=wx.RIGHT, border=8)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.SetInitialSize((400, 150))
        self.Fit()

    def on_ok(self, event):
        self.column_name = self.text_ctrl.GetValue()
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def get_column_data(self):
        return self.column_name


class InsertDataDialog(wx.Dialog):
    def __init__(self, parent, table_name, column_names):
        super(InsertDataDialog, self).__init__(parent, title=f"Insert Data for {table_name}")

        self.table_name = table_name
        self.column_names = column_names
        self.data = {}

        # Create a panel
        panel = wx.Panel(self)

        # Use a box sizer for layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create text controls for each column
        for column_name in self.column_names:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(panel, label=f"{column_name}:")
            hbox.Add(label, proportion=1, flag=wx.RIGHT, border=8)
            text_ctrl = wx.TextCtrl(panel)
            hbox.Add(text_ctrl, proportion=1)
            vbox.Add(hbox, flag=wx.EXPAND|wx.ALL, border=10)
            self.data[column_name] = text_ctrl

        # Add buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_insert = wx.Button(panel, label="Insert")
        btn_insert.Bind(wx.EVT_BUTTON, self.on_insert)
        hbox_buttons.Add(btn_insert, flag=wx.RIGHT, border=8)
        btn_cancel = wx.Button(panel, label="Cancel")
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox_buttons.Add(btn_cancel, flag=wx.RIGHT, border=8)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.SetInitialSize((400, 300))
        self.Fit()

    def get_data(self):
        return {column_name: text_ctrl.GetValue() for column_name, text_ctrl in self.data.items()}

    
    def on_insert(self, event):
        # Get data from text controls
        new_data = {}
        for column_name, text_ctrl in self.data.items():
            new_data[column_name] = text_ctrl.GetValue()

        # Insert data into the table
        try:
            self.GetParent().db.insert_all_data([new_data], self.table_name) 
            wx.MessageBox("Data inserted successfully", "Success", wx.OK | wx.ICON_INFORMATION)
            self.Destroy()
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
    
    
    def on_cancel(self, event):
        self.Destroy()


class DeleteDataDialog(wx.Dialog):
    def __init__(self, parent, table_name, column_names):
        super(DeleteDataDialog, self).__init__(parent, title=f"Delete Data from {table_name}")

        self.table_name = table_name
        self.column_names = column_names
        self.data = {}

        # Create a panel
        panel = wx.Panel(self)

        # Use a box sizer for layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create text controls for each column
        for column_name in self.column_names:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(panel, label=f"{column_name}:")
            hbox.Add(label, proportion=1, flag=wx.RIGHT, border=8)
            text_ctrl = wx.TextCtrl(panel)
            hbox.Add(text_ctrl, proportion=1)
            vbox.Add(hbox, flag=wx.EXPAND|wx.ALL, border=10)
            self.data[column_name] = text_ctrl

        # Add buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_delete = wx.Button(panel, label="Delete")
        btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        hbox_buttons.Add(btn_delete, flag=wx.RIGHT, border=8)
        btn_cancel = wx.Button(panel, label="Cancel")
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox_buttons.Add(btn_cancel, flag=wx.RIGHT, border=8)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.SetInitialSize((400, 300))
        self.Fit()

    def on_delete(self, event):
    # Get data from text controls
        print("-------")
        print("-------")
        delete_data = {}
        for index, (column_name, text_ctrl) in enumerate(self.data.items()):
            value = text_ctrl.GetValue()
            if value:
                delete_data[column_name] = value

        # Delete data from the table
        try:
            if not delete_data:
                raise ValueError("Please provide valid data for deletion")

            message = f"Are you sure you want to delete rows where {' and '.join([f'{k}={v}' for k, v in delete_data.items()])}?"
            if wx.MessageBox(message, "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING) == wx.YES:
                where_conditions = {k: v for k, v in delete_data.items()}
                print(where_conditions)
                print("0")
                self.GetParent().db.delete_data(self.table_name, where_conditions)
                print("a")
                wx.MessageBox("Data deleted successfully", "Success", wx.OK | wx.ICON_INFORMATION)
                print("b")
                self.Destroy()
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)




    def on_cancel(self, event):
        self.Destroy()



class CreateDatabaseDialog(wx.Dialog):
    
    def __init__(self, parent):
        super(CreateDatabaseDialog, self).__init__(parent, title="Create Database")

        self.data = {}
        self.database_name = ""

        # Create a panel
        panel = wx.Panel(self)

        # Use a box sizer for layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create text controls for each column
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, label="Database Name:")
        hbox.Add(label, proportion=1, flag=wx.RIGHT, border=8)
        self.text_ctrl = wx.TextCtrl(panel)
        hbox.Add(self.text_ctrl, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND|wx.ALL, border=10)

        # Add buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_create = wx.Button(panel, label="Create Database")
        btn_create.Bind(wx.EVT_BUTTON, self.on_create)
        hbox_buttons.Add(btn_create, flag=wx.RIGHT, border=8)
        btn_cancel = wx.Button(panel, label="Cancel")
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox_buttons.Add(btn_cancel, flag=wx.RIGHT, border=8)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.SetInitialSize((400, 300))
        self.Fit()

    def on_create(self, event):
        self.database_name = self.text_ctrl.GetValue()
        self.EndModal(wx.ID_OK)
        

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)
        
    def get_input(self):
        return self.database_name
    
    
    
    # Get data from text controls
        # print("-------")
        # print("-------")
        # delete_data = {}
        # for index, (column_name, text_ctrl) in enumerate(self.data.items()):
        #     value = text_ctrl.GetValue()
        #     if value:
        #         delete_data[column_name] = value

        # # Delete data from the table
        # try:
        #     if not delete_data:
        #         raise ValueError("Please provide valid data for deletion")

        #     message = f"Are you sure you want to delete rows where {' and '.join([f'{k}={v}' for k, v in delete_data.items()])}?"
        #     if wx.MessageBox(message, "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING) == wx.YES:
        #         where_conditions = {k: v for k, v in delete_data.items()}
        #         print(where_conditions)
        #         print("0")
        #         self.GetParent().db.delete_data(self.table_name, where_conditions)
        #         print("a")
        #         wx.MessageBox("Data deleted successfully", "Success", wx.OK | wx.ICON_INFORMATION)
        #         print("b")
        #         self.Destroy()
        # except Exception as e:
        #     wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)




    def on_cancel(self, event):
        self.Destroy()




# class GraphPage(wx.Panel):
#     def __init__(self, parent, db, table):
#         super(GraphPage, self).__init__(parent)

#         self.db = db
#         self.table = table
#         self.x_axis_label = ""
#         self.y_axis_label = ""
#         main_sizer = wx.BoxSizer(wx.VERTICAL)

#         # Graph type selection
#         graph_type_choices = ["Bar Graph", "Line Graph"]
#         self.graph_type_choice = wx.Choice(self, choices=graph_type_choices)
#         main_sizer.Add(self.graph_type_choice, flag=wx.EXPAND | wx.ALL, border=10)

#         # X Axis selection
#         self.x_axis_choice = wx.Choice(self)
#         main_sizer.Add(wx.StaticText(self, label="Select X Axis:"), flag=wx.LEFT, border=10)
#         main_sizer.Add(self.x_axis_choice, flag=wx.EXPAND | wx.ALL, border=10)

#         # Y Axis selection
#         self.y_axis_choice = wx.Choice(self)
#         main_sizer.Add(wx.StaticText(self, label="Select Y Axis:"), flag=wx.LEFT, border=10)
#         main_sizer.Add(self.y_axis_choice, flag=wx.EXPAND | wx.ALL, border=10)

#         # Graph display area
#         self.figure, self.ax = plt.subplots()
#         self.canvas = FigureCanvas(self, -1, self.figure)
#         main_sizer.Add(self.canvas, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

#         # Bind events
#         self.graph_type_choice.Bind(wx.EVT_CHOICE, self.on_graph_type_change)
#         self.x_axis_choice.Bind(wx.EVT_CHOICE, self.on_x_axis_change)
#         self.y_axis_choice.Bind(wx.EVT_CHOICE, self.on_y_axis_change)

#         self.SetSizer(main_sizer)

#         # Populate x and y axis choices
#         self.populate_axis_choices()

#     def populate_axis_choices(self):
#         # Get the selected table from the parent notebook
#         parent = self.GetParent()
#         selected_table = self.table_choices.GetStringSelection()
#         if not selected_table:
#             wx.MessageBox("Please select a table", "Error", wx.OK | wx.ICON_ERROR)
#             return

#         try:
#             columns, _ = self.db.execute_query(f"PRAGMA table_info({selected_table})")
#             column_names = [column[1] for column in columns]
#             self.x_axis_choice.SetItems(column_names)
#             self.y_axis_choice.SetItems(column_names)
#         except Exception as e:
#             wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


#     def on_graph_type_change(self, event):
#         self.plot_graph()

#     def on_x_axis_change(self, event):
#         self.x_axis_label = self.x_axis_choice.GetStringSelection()
#         self.plot_graph()

#     def on_y_axis_change(self, event):
#         self.y_axis_label = self.y_axis_choice.GetStringSelection()
#         self.plot_graph()

#     def plot_graph(self):
#         self.ax.clear()
#         data = self.get_selected_table_data()
#         if data is None:
#             return

#         x_values = [str(row[self.x_axis_label]) for row in data]
#         y_values = [float(row[self.y_axis_label]) for row in data]

#         if self.graph_type_choice.GetStringSelection() == "Bar Graph":
#             self.ax.bar(x_values, y_values)
#         elif self.graph_type_choice.GetStringSelection() == "Line Graph":
#             self.ax.plot(x_values, y_values)

#         self.ax.set_xlabel(self.x_axis_label)
#         self.ax.set_ylabel(self.y_axis_label)
#         self.ax.set_title(self.graph_type_choice.GetStringSelection())

#         self.canvas.draw()

#     def get_selected_table_data(self):
#         # Get the selected table from the parent notebook
#         parent = self.GetParent()
#         selected_table = parent.table_choice.GetStringSelection()
#         if not selected_table:
#             wx.MessageBox("Please select a table", "Error", wx.OK | wx.ICON_ERROR)
#             return None

#         try:
#             _, data = self.db.execute_query(f"SELECT * FROM {selected_table}")
#             return data
#         except Exception as e:
#             wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
#             return None


        


class App(wx.App):
    def __init__(self):
        super().__init__()
        
    def OnInit(self):
        frame = MainFrame(None)
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()