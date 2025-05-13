# REFERENCE: https://medium.com/@matheodaly.md/using-google-drive-api-with-python-and-a-service-account-d6ae1f6456c2
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError

# Bard
scope = ['https://www.googleapis.com/auth/drive']
service_account_json_key = '/Users/MATHEO/Downloads/my_key_name.json'
credentials = service_account.Credentials.from_service_account_file(
                              filename=service_account_json_key,
                              scopes=scope)
                              
service = build('drive', 'v3', credentials=credentials)

file_path = 'myfile.txt'
mimetype = 'text/plain'

media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)

body = {
    'name': 'MyUploadedFile.txt',
    'mimeType': mimetype
}

request = service.files().create(body=body, media_body=media)
response = request.execute()
print(f"File uploaded with ID: {response.get('id')}")
