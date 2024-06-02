# FileCat - FTP Client / Filezilla/CyberDuck clone project with Python

FileCat is a simple FTP client application built with Python and Tkinter. It allows users to connect to FTP/SFTP servers, browse remote directories, download files, and upload files or folders to the server (if permission granted). It provides a user-friendly interface for managing files and directories on remote servers.

## Features

- **Connect to FTP/SFTP Servers:** Enter server address, username, password, and port to connect to FTP/SFTP servers.
- **Browse Remote Directories:** Navigate through remote directories to view files and folders.
- **Download Files:** Double-click on a file to download it to the local system.
- **Upload Files/Folders:** Drag and drop files or folders to upload them to the server (if permission granted).
- **Remember Credentials:** Option to remember server credentials for future connections.

## Libraries Used

- **tkinter:** Standard Python interface to the Tk GUI toolkit.
- **ftplib:** Standard Python library for FTP protocol.
- **configparser:** Standard Python library for working with configuration files.
- **os:** Standard Python library for interacting with the operating system.

## Usage

- Launch the application.
- Enter the server address, username, password, and port.
- Click on the "Connect" button to connect to the server.
- Navigate through remote directories using the file explorer.
- Double-click on a file to download it to the local system.
- Upload files to the server (if permission granted).
- Click on the "Disconnect" button to disconnect from the server.

## Classes

### filecat.py

FileCatApp Class:
   - __init__(self, master): Initializes the main application window, including all widgets and their layout.
   - connect(self): Connects to the FTP server using the provided credentials and updates the file explorer.
   - disconnect(self): Disconnects from the FTP server and clears the file explorer.
   - upload_file(self): Opens a file dialog to select a file for uploading to the current directory on the server.


### file_explorer.py

 FileExplorer Class:
   - __init__(self, master): Initializes the file explorer frame, including the tree view for displaying files and folders.
   - update_treeview(self, files): Updates the tree view with the provided list of files and directories.
   - change_directory(self, event=None): Changes the current directory to the specified path and updates the tree view.
   - on_double_click(self, event): Handles double-click events on the tree view, either changing the directory or downloading a file.
   - download_file(self, filename, server_address): Downloads the specified file from the current directory to the local system.
   - up_directory(self): Moves up one directory level in the file explorer.
