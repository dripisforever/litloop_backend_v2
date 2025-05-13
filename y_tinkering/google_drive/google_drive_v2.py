# REFERENCE: https://medium.com/@matheodaly.md/using-google-drive-api-with-python-and-a-service-account-d6ae1f6456c2
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError


scope = ['https://www.googleapis.com/auth/drive']
service_account_json_key = '/Users/MATHEO/Downloads/my_key_name.json'
credentials = service_account.Credentials.from_service_account_file(
                              filename=service_account_json_key,
                              scopes=scope)
service = build('drive', 'v3', credentials=credentials)

# Call the Drive v3 API
results = service.files().list(pageSize=1000, fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)", q='name contains "de"').execute()
# get the results
items = results.get('files', [])


data = []
for row in items:
    if row["mimeType"] != "application/vnd.google-apps.folder":
        row_data = []
        try:
            row_data.append(round(int(row["size"])/1000000, 2))
        except KeyError:
            row_data.append(0.00)
        row_data.append(row["id"])
        row_data.append(row["name"])
        row_data.append(row["modifiedTime"])
        row_data.append(row["mimeType"])
        data.append(row_data)
cleared_df = pd.DataFrame(data, columns = ['size_in_MB', 'id', 'name', 'last_modification', 'type_of_file'])

file_metadata = service.files().get(fileId="your_file_id").execute()

new_permission = {
      'type': 'user',
      'role': 'writer',
      'emailAddress' : 'youremail@gmail.com',
  }
try:
  service.permissions().create(fileId='file_id', body=new_permission, transferOwnership=False).execute()
except (AttributeError, HttpError) as error:
    print(F'An error occurred: {error}')


try:
    request_file = service.files().get_media(fileId="file_id")
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request_file)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(F'Download {int(status.progress() * 100)}.')
except HttpError as error:
    print(F'An error occurred: {error}')

file_retrieved: str = file.getvalue()
with open(f"downloaded_file.csv", 'wb') as f:
    f.write(file_retrieved)

request_file = service.files().export_media(fileId="file_id", mimeType='text/csv').execute()
with open(f"downloaded_file.csv", 'wb') as f:
    f.write(request_file)

service.files().delete(fileId='file_id').execute()

# UPLOAD
file_metadata = {'name': 'filename_on_the_drive.csv'}
media = MediaFileUpload('local_filepath/local_file_name.csv',
                        mimetype='text/csv')

file = service.files().create(body=file_metadata, media_body=media,
                              fields='id').execute()


#
media = MediaFileUpload(
    'local_filepath/local_file_name.csv',
    mimetype='text/csv',
    resumable=True
)
