import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import ftplib
import os
from datetime import datetime

class FileExplorer(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app  # Save reference to FileCatApp instance
        self.ftp = None 
        self.current_path = tk.StringVar()

        self.url_entry = tk.Entry(self)
        self.url_entry.pack(fill=tk.X)
        self.url_entry.bind("<Return>", self.change_directory)
        
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("size", "type") 
        self.tree.heading("#0", text="Name", anchor=tk.W)
        self.tree.heading("size", text="Size", anchor=tk.W)
        self.tree.heading("type", text="Type", anchor=tk.W)
        
        self.tree.column("size", stretch=tk.YES)
        self.tree.column("type", stretch=tk.YES)
        self.url_frame = tk.Frame(self)
        self.url_frame.pack(fill=tk.X)
        self.tree.pack(expand=True, fill=tk.BOTH)
        icon_path = os.path.join(os.path.dirname(__file__), "folder_icon.png")
        self.folder_icon = PhotoImage(file=icon_path)
        up_icon = PhotoImage(file="up_icon.png")
        self.up_button = tk.Button(self.url_frame, image=up_icon, command=self.up_directory)
        self.up_button.image = up_icon
        self.up_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Add delete button
        self.delete_button = tk.Button(self.url_frame, text="Delete", command=self.delete_item)
        self.delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Add reconnect button
        self.reconnect_button = tk.Button(self.url_frame, text="Reconnect", command=self.reconnect)
        self.reconnect_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Add upload button next to delete button
        self.app.upload_button = tk.Button(self.url_frame, text="Upload", command=self.app.upload, state=tk.DISABLED)
        self.app.upload_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def update_treeview(self, files):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ("size", "type", "last_modified")
        self.tree.heading("size", text="Size", anchor=tk.W)
        self.tree.heading("type", text="Type", anchor=tk.W)
        self.tree.heading("last_modified", text="Last Modified", anchor=tk.W)

        directories = []
        files_list = []

        for name, details in files:
            if details['type'] == 'dir':
                directories.append((name, details))
            else:
                files_list.append((name, details))

        for name, details in directories:
            last_modified = self._format_last_modified(details.get('modify', ''))
            self.tree.insert("", "end", text=name, open=False, image=self.folder_icon,
                            values=("", "Directory", last_modified))

        for name, details in files_list:
            size_kb = int(details.get('size', 0)) / 1024
            last_modified = self._format_last_modified(details.get('modify', ''))
            self.tree.insert("", "end", values=(f"{size_kb:.2f} KB", "File", last_modified), text=name)
    
    def delete_item(self):
        item_id = self.tree.selection()[0]
        item = self.tree.item(item_id)
        item_text = item["text"]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_text}'?"):
            try:
                if item["values"][1] == "File":
                    self.ftp.delete(os.path.join(self.current_path.get(), item_text))
                elif "directory" in item["tags"]:
                    self.ftp.rmd(os.path.join(self.current_path.get(), item_text))
                self.change_directory()
            except ftplib.error_perm as e:
                messagebox.showerror("Error", str(e))

    def reconnect(self):
        self.app.reconnect()  # Use the FileCatApp instance to call connect method
    
    def _format_last_modified(self, raw_timestamp):
        try:
            timestamp = datetime.strptime(raw_timestamp, "%Y%m%d%H%M%S")
            formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            return formatted_date
        except ValueError:
            return ""

    def change_directory(self, event=None):
        new_path = self.url_entry.get().strip()

        new_path = new_path.replace("\\", "/")

        if not new_path.startswith("/"):
            new_path = "/" + new_path

        try:
            files = self.ftp.mlsd(new_path)
            files = [(name, details) for name, details in files if name not in ['.', '..']]

            self.current_path.set(new_path)
            self.update_treeview(files)
        except ftplib.error_perm as e:
            messagebox.showerror("Error", str(e))

    def on_double_click(self, event):
        item_id = self.tree.focus()
        item = self.tree.item(item_id)
        item_text = item["text"]
        item_type = item["values"][1]

        if item_text != "":
            if item_type == "Directory":
                self.url_entry.delete(0, tk.END)
                new_path = os.path.join(self.current_path.get(), item_text)
                self.url_entry.insert(0, new_path)
                self.change_directory()
            elif item_type == "File":
                self.download_file(item_text)

    def up_directory(self):
        current_path = self.url_entry.get().strip()
        if current_path != "/":
            parent_path = os.path.dirname(current_path)
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, parent_path)
            self.change_directory()
    
    def download_file(self, filename):
        remote_filename = os.path.join(self.current_path.get(), filename)
        remote_filename = remote_filename.replace("\\", "/")

        downloads_folder = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)

        local_filename = os.path.join(downloads_folder, filename)

        with open(local_filename, 'wb') as local_file:
            try:
                self.ftp.retrbinary('RETR ' + remote_filename, local_file.write)
                messagebox.showinfo("Download", f"{filename} downloaded successfully.")
            except ftplib.error_perm as e:
                messagebox.showerror("Download Error", f"Failed to download {filename}: {str(e)}")
