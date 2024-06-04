import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

def list_drive_files(service):
    """Lists files on the user's Google Drive."""
    try:
        results = service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name)",
            q="trashed=false"
        ).execute()
        
        items = results.get('files', [])
        
        if not items:
            print("No existing file found in Drive.")
            return {}
        else:
            print("Existing Files in Drive:")
            file_dict = {}
            for item in items:
                file_name = item['name']
                file_id = item['id']
                if file_name not in file_dict:
                    file_dict[file_name] = file_id
            
            return file_dict
    except HttpError as error:
        print(f"Error: {error}")
        return {}


def upload_file(service, file_path, mime_type):
    """Uploads a file to Google Drive."""
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    try:
        file = service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        print(f"File ID: {file.get('id')}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def download_file(service, file_id, file_path):
    """Downloads a file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

def delete_file(service,file_id):
    """Deletes a file from Google Drive."""
    body_value = {'trashed': True}
    response = service.files().update(fileId=file_id, body=body_value).execute()
    return response

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        file_dict = list_drive_files(service)
    
        for file_name, file_id in file_dict.items():
            print(f"{file_name} ({file_id})")

        # Upload a file
        file_pathU = '' 
        mime_type = ''  
        #upload_file(service, file_pathU, mime_type)

        # Download a file 
        file_id = ""
        file_pathD = ''
        #download_file(service, file_id, file_pathD)

        #delete_file(service,"file id" )

    except HttpError as error:
        # TODO - Handle errors from drive API.
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
