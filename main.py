from __future__ import print_function
from collections import namedtuple
from binascii import unhexlify
import sys
import numpy as np
import pickle
import binascii
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


CHUNK_SIZE = 500000 # 1 = one byte; 500000 bytes = 500 kb

def main():
    file = open(sys.argv[1], 'rb')
    service_docs = google_docs_api_login()
    service_files = google_files_api_login()

    #upload_file(service_docs, file)
    download_file(service_docs, service_files, file)


def download_file(service_docs, service_files, file_name):
    file_name = file_name.name
    results = service_files.files().list(pageSize=100, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files in Google Drive found.')
    else:
        to_download_drive_file = namedtuple("to_download_drive_file", "id name count type")
        to_download_drive_files = []
        for item in items:
            drive_file_name = item['name']
            drive_file_id = item['id']

            drive_file_name_urg = drive_file_name.split('-')[0]
            drive_file_name_count = drive_file_name.split('-')[1]
            drive_file_name_type = drive_file_name.split('.')[1].split('-')[0]
            if drive_file_name_urg == file_name:
                to_download_drive_files.append(to_download_drive_file(drive_file_id, drive_file_name_urg, drive_file_name_count, drive_file_name_type))
    to_download_drive_files_ordered = []
    itr = 1
    break_ = False
    while True:
        if break_:
            break
        for i in range(len(to_download_drive_files)):
            if int(to_download_drive_files[i].count) == int(itr):
                to_download_drive_files_ordered.append(to_download_drive_file(to_download_drive_files[i].id, to_download_drive_files[i].name, to_download_drive_files[i].count, to_download_drive_files[i].type))
                if int(itr) == int(len(to_download_drive_files)):
                    break_=True
                itr += 1

    newFile = open('downloads/'+file_name, "wb")
    for i in range(len(to_download_drive_files_ordered)):
        print('Name:', to_download_drive_files_ordered[i].name, 'ID: ', to_download_drive_files_ordered[i].id, 'Type:', to_download_drive_files_ordered[i].type, 'Count:', to_download_drive_files_ordered[i].count)

        document = service_docs.documents().get(documentId=str(to_download_drive_files_ordered[i].id)).execute()
        content = document.get('body').get('content')[1].get('paragraph').get('elements')[0].get('textRun').get('content')
        print(content)
        newFile.write(bytearray.fromhex(content[:-1]))
        #print()

def upload_file(service, file):
    chunk_it = 0
    for chunk in read_in_chunks(file):
        chunk_it += 1
        title = file.name+'-'+str(chunk_it)
        body = {
            'title': title
        }
        doc = service.documents().create(body=body).execute()
        chunk_preped = str(binascii.b2a_hex(chunk))[2:-1]
        print('Uploading data chunk[',chunk_it,']')
        requests = [
             {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': chunk_preped
                }
            }
        ]
        result = service.documents().batchUpdate(documentId=doc.get('documentId'), body={'requests': requests}).execute()

def google_docs_api_login():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_docs.pickle'):
        with open('token_docs.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/documents'])
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token_docs.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('docs', 'v1', credentials=creds)

def google_files_api_login():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_files.pickle'):
        with open('token_files.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow_drive = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive'])
            creds = flow_drive.run_local_server()
        # Save the credentials for the next run
        with open('token_files.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def read_in_chunks(infile):
    while True:
        chunk = infile.read(CHUNK_SIZE)
        if chunk:
            yield chunk
        else:
            return

if __name__== "__main__":
  main()
