import requests
from msal import ConfidentialClientApplication

class OneDriveService:
    def __init__(self, client_id, client_secret, tenant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.token = self.get_token()

    def get_token(self):
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = ConfidentialClientApplication(self.client_id, authority=authority, client_credential=self.client_secret)
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        return result['access_token']

    def list_files(self, folder_id):
        headers = {'Authorization': 'Bearer ' + self.token}
        endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def upload_file(self, folder_id, file_path):
        headers = {'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/octet-stream'}
        endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}:/{file_path.split('/')[-1]}:/content"
        with open(file_path, 'rb') as file:
            response = requests.put(endpoint, headers=headers, data=file)
        return response.json()

    def download_file(self, file_id, output_path):
        headers = {'Authorization': 'Bearer ' + self.token}
        endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
        response = requests.get(endpoint, headers=headers)
        with open(output_path, 'wb') as file:
            file.write(response.content)
        return output_path