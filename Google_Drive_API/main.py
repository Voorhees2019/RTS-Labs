# https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_MIME-%D1%82%D0%B8%D0%BF%D0%BE%D0%B2
from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
from apiclient import errors
from Google_Drive_API import auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
auth_instance = auth.Auth(SCOPES)
creds = auth_instance.get_credentials()
drive_service = build('drive', 'v3', credentials=creds)


def list_files(size):
    # Call the Drive v3 API
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


# list_files(300)


def upload_file(filename, filepath, mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


# the list of mime types:

# upload_file('test1.txt', 'test1.txt', 'text/plain')


def download_file(file_id, filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    # to save the file
    with io.open(filepath, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())


# download_file('1tCgfvYgvkwDpeVkTpb-rzVRepHNuG3eQ', 'something_here.txt')


def create_folder(name):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print('Folder ID: %s' % file.get('id'))


# create_folder('new one')


def insert_file_in_folder(filename, filepath, mimetype, folder_id):
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(filepath,
                            mimetype=mimetype,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return f'{file.get("id")}'


# insert_file_in_folder('test1.txt', 'test1.txt', 'text/plain', '1XaC6ZiN3NsDgBJcueTeGoHIEDO8VyGOv')


def move_file_between_folders(file_id, new_folder_id):
    # Retrieve the existing parents to remove
    file = drive_service.files().get(fileId=file_id,
                                     fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    # Move the file to the new folder
    file = drive_service.files().update(fileId=file_id,
                                        addParents=new_folder_id,
                                        removeParents=previous_parents,
                                        fields='id, parents').execute()


# move_file_between_folders('1Mgvb1rVEec6ElukiuT-nnd-46WtIpjyx', '1XaC6ZiN3NsDgBJcueTeGoHIEDO8VyGOv')


def search_files(size, query):
    # Call the Drive v3 API
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)", q=query).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


# search_files(10, "name contains 'test'")
# the following query string filters the search to just return folders with name='test folder'
# search_files(10, "name='test folder' and mimeType='application/vnd.google-apps.folder'")


def delete_file(file_id, service=drive_service):
    """ Permanently delete a file, skipping the trash.
    Args:
            service: Drive API service instance.
            file_id: ID of the file to delete.
    """
    try:
        service.files().delete(fileId=file_id).execute()
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


