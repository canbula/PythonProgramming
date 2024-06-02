import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
import sqlite3

class SQLiteBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Database Browser Clone")
        self.conn = None

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.db_label = tk.Label(frame, text="Database:")
        self.db_label.grid(row=0, column=0, sticky='e')

        self.db_entry = tk.Entry(frame, width=50)
        self.db_entry.grid(row=0, column=1)

        self.browse_button = tk.Button(frame, text="Browse", command=self.browse_db)
        self.browse_button.grid(row=0, column=2, padx=5)

        self.connect_button = tk.Button(frame, text="Connect", command=self.connect_to_db)
        self.connect_button.grid(row=0, column=3, padx=5)

        self.create_db_button = tk.Button(frame, text="Create Database", command=self.create_db)
        self.create_db_button.grid(row=0, column=4, padx=5)

        self.query_label = tk.Label(frame, text="SQL Query:")
        self.query_label.grid(row=1, column=0, sticky='nw', pady=10)

        self.query_text = tk.Text(frame, width=80, height=10)
        self.query_text.grid(row=2, column=0, columnspan=6, pady=10)

        self.execute_button = tk.Button(frame, text="Execute Query", command=self.execute_query)
        self.execute_button.grid(row=3, column=0, columnspan=6, pady=5)

        self.result_text = tk.Text(frame, width=80, height=15)
        self.result_text.grid(row=4, column=0, columnspan=6, pady=10)

        self.tables_button = tk.Button(frame, text="Show Tables", command=self.show_tables)
        self.tables_button.grid(row=5, column=0, columnspan=6, pady=5)

        self.structure_button = tk.Button(frame, text="Database Structure", command=self.show_structure)
        self.structure_button.grid(row=6, column=0, columnspan=6, pady=5)

        self.view_data_button = tk.Button(frame, text="View Data", command=self.view_data)
        self.view_data_button.grid(row=7, column=0, columnspan=6, pady=5)

    def browse_db(self):
        db_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
        if db_path:
            self.db_entry.delete(0, tk.END)
            self.db_entry.insert(0, db_path)

    def connect_to_db(self):
        db_name = self.db_entry.get()
        try:
            self.conn = sqlite3.connect(db_name)
            messagebox.showinfo("Connection", "Connected to the database successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def create_db(self):
        db_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")])
        if db_path:
            try:
                conn = sqlite3.connect(db_path)
                conn.close()
                messagebox.showinfo("Create Database", "Database created successfully.")
                self.db_entry.delete(0, tk.END)
                self.db_entry.insert(0, db_path)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def execute_query(self):
        if not self.conn:
            messagebox.showwarning("Warning", "Please connect to a database first.")
            return

        query = self.query_text.get("1.0", tk.END).strip()
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            if query.lower().startswith("select"):
                results = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                self.display_results(results, columns)
            else:
                self.conn.commit()
                messagebox.showinfo("Success", "Query executed successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cursor.close()

    def display_results(self, results, columns):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "\t".join(columns) + "\n")
        self.result_text.insert(tk.END, "-" * 80 + "\n")
        for row in results:
            self.result_text.insert(tk.END, "\t".join(map(str, row)) + "\n")

    def show_tables(self):
        if not self.conn:
            messagebox.showwarning("Warning", "Please connect to a database first.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Tables in the database:\n")
            self.result_text.insert(tk.END, "-" * 80 + "\n")
            for table in tables:
                self.result_text.insert(tk.END, table[0] + "\n")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cursor.close()

    def show_structure(self):
        if not self.conn:
            messagebox.showwarning("Warning", "Please connect to a database first.")
            return

        StructureWindow(self.root, self.conn)

    def view_data(self):
        if not self.conn:
            messagebox.showwarning("Warning", "Please connect to a database first.")
            return

        ViewDataWindow(self.root, self.conn)

    def open_create_table_window(self):
        if not self.conn:
            messagebox.showwarning("Warning", "Please connect to a database first.")
            return

        CreateTableWindow(self.root, self.conn)

    def on_closing(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()

class CreateTableWindow:
    def __init__(self, parent, conn):
        self.conn = conn
        self.window = tk.Toplevel(parent)
        self.window.title("Create Table")
        self.columns = []

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.table_name_label = tk.Label(frame, text="Table Name:")
        self.table_name_label.grid(row=0, column=0, sticky='e')

        self.table_name_entry = tk.Entry(frame, width=30)
        self.table_name_entry.grid(row=0, column=1, pady=5)

        self.add_column_button = tk.Button(frame, text="Add Column", command=self.add_column)
        self.add_column_button.grid(row=0, column=2, padx=5)

        self.columns_frame = tk.Frame(frame)
        self.columns_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.sql_text = tk.Text(frame, width=60, height=5, state=tk.DISABLED)
        self.sql_text.grid(row=2, column=0, columnspan=3, pady=10)

        self.create_table_button = tk.Button(frame, text="Create Table", command=self.create_table)
        self.create_table_button.grid(row=3, column=0, columnspan=3, pady=5)

    def add_column(self):
        column_frame = tk.Frame(self.columns_frame)
        column_frame.pack(fill=tk.X, pady=2)

        column_name_entry = tk.Entry(column_frame, width=20)
        column_name_entry.pack(side=tk.LEFT, padx=5)

        column_type_var = tk.StringVar()
        column_type_menu = ttk.Combobox(column_frame, textvariable=column_type_var, values=["INTEGER", "TEXT", "REAL", "BLOB", "NUMERIC"], width=10)
        column_type_menu.pack(side=tk.LEFT, padx=5)
        column_type_menu.current(0)

        not_null_var = tk.IntVar()
        not_null_check = tk.Checkbutton(column_frame, text="NOT NULL", variable=not_null_var)
        not_null_check.pack(side=tk.LEFT, padx=5)

        primary_key_var = tk.IntVar()
        primary_key_check = tk.Checkbutton(column_frame, text="PRIMARY KEY", variable=primary_key_var)
        primary_key_check.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(column_frame, text="Remove", command=lambda: self.remove_column(column_frame))
        remove_button.pack(side=tk.LEFT, padx=5)

        column_info = (column_name_entry, column_type_var, not_null_var, primary_key_var)
        self.columns.append(column_info)

        self.update_sql()

    def remove_column(self, column_frame):
        column_frame.destroy()
        self.columns = [col for col in self.columns if col[0].winfo_exists()]
        self.update_sql()

    def update_sql(self):
        table_name = self.table_name_entry.get().strip()
        if not table_name:
            return

        columns_def = []
        for column_info in self.columns:
            col_name = column_info[0].get().strip()
            col_type = column_info[1].get()
            col_not_null = column_info[2].get()
            col_primary_key = column_info[3].get()
            if col_name:
                column_def = f"{col_name} {col_type}"
                if col_not_null:
                    column_def += " NOT NULL"
                if col_primary_key:
                    column_def += " PRIMARY KEY"
                columns_def.append(column_def)

        if columns_def:
            create_table_sql = f"CREATE TABLE {table_name} ({', '.join(columns_def)});"
            self.sql_text.config(state=tk.NORMAL)
            self.sql_text.delete("1.0", tk.END)
            self.sql_text.insert(tk.END, create_table_sql)
            self.sql_text.config(state=tk.DISABLED)

    def create_table(self):
        create_table_sql = self.sql_text.get("1.0", tk.END).strip()
        cursor = self.conn.cursor()

        try:
            cursor.execute(create_table_sql)
            self.conn.commit()
            messagebox.showinfo("Success", "Table created successfully.")
            self.window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cursor.close()

class StructureWindow:
    def __init__(self, parent, conn):
        self.conn = conn
        self.window = tk.Toplevel(parent)
        self.window.title("Database Structure")

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tables_listbox = tk.Listbox(frame, width=50, height=20)
        self.tables_listbox.grid(row=0, column=0, padx=5, pady=5)

        self.modify_table_button = tk.Button(frame, text="Modify Table", command=self.modify_table)
        self.modify_table_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_table_button = tk.Button(frame, text="Delete Table", command=self.delete_table)
        self.delete_table_button.grid(row=0, column=2, padx=5, pady=5)

        self.add_table_button = tk.Button(frame, text="Add Table", command=self.add_table)
        self.add_table_button.grid(row=0, column=3, padx=5, pady=5)

        self.show_structure()

    def show_structure(self):
        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                self.tables_listbox.insert(tk.END, table[0])
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cursor.close()

    def modify_table(self):
        selected_table = self.tables_listbox.get(tk.ACTIVE)
        if selected_table:
            ModifyTableWindow(self.window, self.conn, selected_table)

    def delete_table(self):
        selected_table = self.tables_listbox.get(tk.ACTIVE)
        if selected_table:
            confirm = messagebox.askyesno("Delete Table", f"Are you sure you want to delete the table '{selected_table}'?")
            if confirm:
                cursor = self.conn.cursor()
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {selected_table};")
                    self.conn.commit()
                    messagebox.showinfo("Success", f"Table '{selected_table}' deleted successfully.")
                    self.tables_listbox.delete(tk.ACTIVE)
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
                finally:
                    cursor.close()

    def add_table(self):
        CreateTableWindow(self.window, self.conn)
class ModifyTableWindow:
    def __init__(self, parent, conn, table_name):
        self.conn = conn
        self.table_name = table_name
        self.window = tk.Toplevel(parent)
        self.window.title(f"Modify Table: {table_name}")
        self.columns = []
        self.existing_columns = []

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.table_name_label = tk.Label(frame, text=f"Table: {self.table_name}")
        self.table_name_label.grid(row=0, column=0, columnspan=2)

        self.add_column_button = tk.Button(frame, text="Add Column", command=self.add_column)
        self.add_column_button.grid(row=0, column=2, padx=5)

        self.columns_frame = tk.Frame(frame)
        self.columns_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.sql_text = tk.Text(frame, width=60, height=5, state=tk.DISABLED)
        self.sql_text.grid(row=2, column=0, columnspan=3, pady=10)

        self.modify_table_button = tk.Button(frame, text="Modify Table", command=self.modify_table)
        self.modify_table_button.grid(row=3, column=0, columnspan=3, pady=5)

        self.load_table_structure()

    def load_table_structure(self):
        cursor = self.conn.cursor()

        try:
            cursor.execute(f"PRAGMA table_info({self.table_name});")
            columns = cursor.fetchall()
            for column in columns:
                self.add_column(existing=True, column=column)
                self.existing_columns.append(column[1])
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cursor.close()

    def add_column(self, existing=False, column=None):
        column_frame = tk.Frame(self.columns_frame)
        column_frame.pack(fill=tk.X, pady=2)

        column_name_entry = tk.Entry(column_frame, width=20)
        column_name_entry.pack(side=tk.LEFT, padx=5)
        if existing:
            column_name_entry.insert(0, column[1])
            column_name_entry.config(state=tk.DISABLED)

        column_type_var = tk.StringVar()
        column_type_menu = ttk.Combobox(column_frame, textvariable=column_type_var, values=["INTEGER", "TEXT", "REAL", "BLOB", "NUMERIC"], width=10)
        column_type_menu.pack(side=tk.LEFT, padx=5)
        if existing:
            column_type_menu.set(column[2])
            column_type_menu.config(state=tk.DISABLED)
        else:
            column_type_menu.current(0)

        not_null_var = tk.IntVar()
        not_null_check = tk.Checkbutton(column_frame, text="NOT NULL", variable=not_null_var)
        not_null_check.pack(side=tk.LEFT, padx=5)
        if existing and column[3]:
            not_null_check.select()
            not_null_check.config(state=tk.DISABLED)

        primary_key_var = tk.IntVar()
        primary_key_check = tk.Checkbutton(column_frame, text="PRIMARY KEY", variable=primary_key_var)
        primary_key_check.pack(side=tk.LEFT, padx=5)
        if existing and column[5]:
            primary_key_check.select()
            primary_key_check.config(state=tk.DISABLED)

        if not existing:
            remove_button = tk.Button(column_frame, text="Remove", command=lambda: self.remove_column(column_frame))
            remove_button.pack(side=tk.LEFT, padx=5)

        column_info = (column_name_entry, column_type_var, not_null_var, primary_key_var)
        self.columns.append(column_info)

        self.update_sql()

    def remove_column(self, column_frame):
        column_frame.destroy()
        self.columns = [col for col in self.columns if col[0].winfo_exists()]
        self.update_sql()

    def update_sql(self):
        table_name = self.table_name
        columns_def = []
        existing_columns = []

        for column_info in self.columns:
            col_name = column_info[0].get().strip()
            col_type = column_info[1].get()
            col_not_null = column_info[2].get()
            col_primary_key = column_info[3].get()
            if col_name:
                column_def = f"{col_name} {col_type}"
                if col_not_null:
                    column_def += " NOT NULL"
                if col_primary_key:
                    column_def += " PRIMARY KEY"
                columns_def.append(column_def)
                existing_columns.append(col_name)

        if columns_def:
            columns_def_str = ", ".join(columns_def)
            create_table_sql = f"CREATE TABLE new_{table_name} ({columns_def_str});"
            self.sql_text.config(state=tk.NORMAL)
            self.sql_text.delete("1.0", tk.END)
            self.sql_text.insert(tk.END, create_table_sql)
            self.sql_text.config(state=tk.DISABLED)

    def modify_table(self):
        create_table_sql = self.sql_text.get("1.0", tk.END).strip()
        cursor = self.conn.cursor()

        try:
            cursor.execute(create_table_sql)

            existing_columns_str = ", ".join(self.existing_columns)
            cursor.execute(f"INSERT INTO new_{self.table_name} ({existing_columns_str}) SELECT {existing_columns_str} FROM {self.table_name};")
            cursor.execute(f"DROP TABLE {self.table_name};")
            cursor.execute(f"ALTER TABLE new_{self.table_name} RENAME TO {self.table_name};")

            self.conn.commit()
            messagebox.showinfo("Success", "Table modified successfully.")
            self.window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cursor.close()

class ViewDataWindow:
    def __init__(self, parent, conn):
        self.conn = conn
        self.window = tk.Toplevel(parent)
        self.window.title("View Data")

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tables_listbox = tk.Listbox(frame, width=50, height=20)
        self.tables_listbox.grid(row=0, column=0, padx=5, pady=5)

        self.view_data_button = tk.Button(frame, text="View Data", command=self.view_data)
        self.view_data_button.grid(row=0, column=1, padx=5, pady=5)

        self.data_text = tk.Text(frame, width=80, height=20)
        self.data_text.grid(row=1, column=0, columnspan=2, pady=10)

        self.load_tables()

    def load_tables(self):
        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                self.tables_listbox.insert(tk.END, table[0])
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cursor.close()

    def view_data(self):
        selected_table = self.tables_listbox.get(tk.ACTIVE)
        if selected_table:
            cursor = self.conn.cursor()
            try:
                cursor.execute(f"SELECT * FROM {selected_table};")
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()

                self.data_text.config(state=tk.NORMAL)
                self.data_text.delete("1.0", tk.END)
                self.data_text.insert(tk.END, f"Table: {selected_table}\n\n")
                self.data_text.insert(tk.END, "\t".join(columns) + "\n")
                self.data_text.insert(tk.END, "-" * 80 + "\n")
                for row in rows:
                    self.data_text.insert(tk.END, "\t".join(map(str, row)) + "\n")
                self.data_text.config(state=tk.DISABLED)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                cursor.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLiteBrowserApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()