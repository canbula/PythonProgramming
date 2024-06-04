import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

class DriveService:
    def __init__(self, client_secrets_file='credentials.json', token_file='token.json', scopes=['https://www.googleapis.com/auth/drive']):
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file
        self.scopes = scopes
        self.service = self.create_drive_service()

    def create_drive_service(self):
        creds = None
        # Token dosyası mevcutsa yükleyin
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        # Token mevcut değilse veya geçersizse, kullanıcı kimlik doğrulaması yapın
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
                creds = flow.run_local_server(port=0)
            # Yeni tokenı kaydedin
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        return build('drive', 'v3', credentials=creds)

    def get_folder_id(self, folder_name_or_path):
        folder_id = 'root'  # Default to root
        if folder_name_or_path not in ['/', '\\', '']:
            folder_id = self.search_folder_id(folder_name_or_path)
        return folder_id

    def search_folder_id(self, folder_name_or_path):
        query = f"name = '{folder_name_or_path}' and mimeType = 'application/vnd.google-apps.folder' and trashed=false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        if items:
            return items[0]['id']
        else:
            print(f"Folder '{folder_name_or_path}' not found.")
            return None
    def get_file_id(self, file_name_or_path):
        file_id = self.search_file_id(file_name_or_path)
        return file_id

    def search_file_id(self, file_name_or_path):
        query = f"name = '{file_name_or_path}' and mimeType != 'application/vnd.google-apps.folder' and trashed=false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        if items:
            return items[0]['id']
        else:
            print(f"File '{file_name_or_path}' not found.")
            return None
    def open_folder(self, folder_name_or_path):
        folder_name_or_path = folder_name_or_path.replace('/', '')
        folder_id = self.get_folder_id(folder_name_or_path)
        if folder_id is None:
            return []

        query = f"'{folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, pageSize=100, fields="files(id, name, size, modifiedTime)").execute()
        items = results.get('files', [])
        dosya_dict_listesi = []

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for idx, item in enumerate(items, start=1):
                filename = item.get('name')
                file_id = item.get('id')
                size = item.get('size', '0')
                modified_time = item.get('modifiedTime', 'N/A')
                dosya_dict = {
                    "Sira": idx,
                    "FileName": filename,
                    "TimeStamp": modified_time,
                    "Size": f"{size} Byte"
                }
                dosya_dict_listesi.append(dosya_dict)
        
        return dosya_dict_listesi

    def dosya_yukle(self,server_path, file_path):
        mime_type='application/octet-stream'
        server_path =server_path.split("/")[1]
        print("mainn",server_path)
        folder_id = self.get_folder_id(server_path)
        file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded file with ID {file.get('id')}")

    def dosya_indir(self, file_path, output_file):
        file_name = file_path.split('/')[-1]
        file_name = file_name.replace("/", "")
        file_id = self.get_file_id(file_name)
        request = self.service.files().get_media(fileId=file_id)
        with open(output_file, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
        print(f"Downloaded file to {output_file}")

    def dosya_sil(self, file_path):
        file_name = file_path.split('/')[-1]
        file_name = file_name.replace("/", "")
        file_id = self.get_file_id(file_name)
        self.service.files().delete(fileId=file_id).execute()
        print(f"Deleted file with ID {file_id}")

#drive_service = DriveService()
#if __name__ == '__main__':
 #  print(drive_service.list_files("/"))
    
    #drive_service.upload_file("test.txt")
#drive bağlantısı var denendi
#dosya yükleme var denendi
#klasör yapısı farklı 
