from __future__ import print_function
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
    service = google_api_login()
    request = service.documents().get(documentId='README.md-1').execute()
    sheets = request.get('sheets', '')
    title = sheets[0].get("properties", {}).get("README.md-1", "README.md-1")
    sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)

    #upload_file(service, file)
    #download_file(service, 'README.md')

def download_file(service, file_name):
    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId='1FEdUH4ma5JRB7TF3UxCwtdH4v2i60ubwD-OjULIR6-o').execute()
    sheets = document.get('sheets', '')
    title = service.documents().get("properties", {}).get("title", "README.md-1")
    print(title)
    sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)

    print(document.get('body').get('content')[1].get('paragraph').get('elements')[0].get('textRun').get('content'))

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

def google_api_login():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/documents'])
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('docs', 'v1', credentials=creds)

def read_in_chunks(infile):
    while True:
        chunk = infile.read(CHUNK_SIZE)
        if chunk:
            yield chunk
        else:
            return

if __name__== "__main__":
  main()
