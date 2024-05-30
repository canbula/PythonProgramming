import tkinter as tk
from tkinter import ttk, messagebox
import ftplib
import configparser
import tkinter.filedialog as filedialog
import os

from file_explorer import FileExplorer

class FileCatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("FileCat - FTP Client")
        self.master.geometry("800x600")
        
        self.connection_frame = tk.Frame(self.master)
        self.connection_frame.pack(fill=tk.X)
        self.upload_button = tk.Button(self.connection_frame, text="Upload", command=self.upload, state=tk.DISABLED)

        tk.Label(self.connection_frame, text="Server Address:").grid(row=0, column=0, padx=5, pady=5)
        self.server_address_entry = tk.Entry(self.connection_frame)
        self.server_address_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Username:").grid(row=0, column=2, padx=5, pady=5)
        self.username_entry = tk.Entry(self.connection_frame)
        self.username_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.connection_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Port:").grid(row=1, column=2, padx=5, pady=5)
        self.port_entry = tk.Entry(self.connection_frame)
        self.port_entry.grid(row=1, column=3, padx=5, pady=5)

        self.remember_var = tk.IntVar(value=0)
        self.remember_checkbox = tk.Checkbutton(self.connection_frame, text="Remember", variable=self.remember_var)
        self.remember_checkbox.grid(row=0, column=4, rowspan=2, padx=5, pady=5)

        self.connect_button = tk.Button(self.connection_frame, text="Connect", command=self.connect)
        self.connect_button.grid(row=0, column=5, padx=5, pady=5)

        self.disconnect_button = tk.Button(self.connection_frame, text="Disconnect", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.grid(row=0, column=6, padx=5, pady=5)

        self.file_explorer = FileExplorer(self.master, self)
        self.file_explorer.pack(expand=True, fill=tk.BOTH)

        self.config = configparser.ConfigParser()
        self.config.read("credentials.ini")
        if "Credentials" in self.config:
            self.server_address_entry.insert(0, self.config["Credentials"].get("ServerAddress", ""))
            self.username_entry.insert(0, self.config["Credentials"].get("Username", ""))
            self.password_entry.insert(0, self.config["Credentials"].get("Password", ""))
            self.port_entry.insert(0, self.config["Credentials"].get("Port", ""))

    def upload(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.upload_file(file_path)

    def reconnect(self):
        self.disconnect()
        self.connect()

    def connect(self):
        server_address = self.server_address_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        port_entry = self.port_entry.get()

        if port_entry:
            try:
                port = int(port_entry)
            except ValueError:
                messagebox.showerror("Connection Error", "Invalid port number.")
                return
        else:
            port = 21

        try:
            ftp = ftplib.FTP()
            ftp.connect(server_address, port)
            ftp.login(username, password)

            self.file_explorer.ftp = ftp

            root_dir = "/"
            self.file_explorer.url_entry.insert(0, root_dir)
            self.file_explorer.change_directory()  
            self.upload_button.config(state=tk.NORMAL)

            self.disconnect_button.config(state=tk.NORMAL)
            self.connect_button.config(state=tk.DISABLED)

            if self.remember_var.get() == 1:
                self.config["Credentials"] = {
                    "ServerAddress": server_address,
                    "Username": username,
                    "Password": password,
                    "Port": port
                }
                with open("credentials.ini", "w") as configfile:
                    self.config.write(configfile)

        except ftplib.all_errors as e:
            messagebox.showerror("Connection Error", str(e))

    def disconnect(self):
        self.upload_button.config(state=tk.DISABLED)
        if self.file_explorer.ftp:
            self.file_explorer.ftp.quit()
            self.file_explorer.ftp = None

            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)

            self.file_explorer.update_treeview([])

            self.file_explorer.url_entry.delete(0, tk.END)

        else:
            messagebox.showinfo("Info", "Not connected to any server.")

    def upload_file(self, file_path):
        file_name = os.path.basename(file_path)

        try:
            with open(file_path, 'rb') as file:
                self.file_explorer.ftp.storbinary('STOR ' + file_name, file)
                messagebox.showinfo("Upload", f"{file_name} uploaded successfully.")
        except Exception as e:
            messagebox.showerror("Upload Error", f"Failed to upload {file_name}: {str(e)}")

def main():
    root = tk.Tk()
    app = FileCatApp(root)
    root.iconbitmap("app.ico") 
    root.mainloop()

if __name__ == "__main__":
    main()
