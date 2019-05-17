from __future__ import print_function
import sys
import numpy as np
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


CHUNK_SIZE = 9000 # 1 = one byte; 9000 bytes = 9 kb

def main():
    file = open(sys.argv[1], 'rb')
    service = google_api_login()

    upload_file(service, file)

def upload_file(service, file):
    chunk_it = 0
    for chunk in read_in_chunks(file):
        chunk_it += 1
        title = file.name+'-'+str(chunk_it)
        body = {
            'title': title
        }
        doc = service.documents().create(body=body).execute()
        requests = [
             {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': chunk
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/documents'])
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
