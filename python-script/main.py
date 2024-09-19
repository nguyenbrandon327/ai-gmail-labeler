import os.path
import base64
import requests
import spacy
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

nlp = spacy.load("en_core_web_sm")

SCOPES = 
[
    'https://www.googleapis.com/auth/gmail.modify',  # read, modify, and delete
    'https://www.googleapis.com/auth/gmail.labels'   # edit labels
]

#function processes each entity within the document tied to the content, then
# prints the entity and the label associated with it
def process_content(content):
     doc = nlp(content)
     for ent in doc.ents:
          print(ent.text, ent.label_)

#function fetches the mail from the user's inbox, then processes the content
def fetch_mail():
     creds = None
     if os.path.exists('token.json'):
          creds = Credentials.from_authorized_user_file('token.json')
     if not creds or not creds.valid:
          creds.refresh(Request())
     
     with open('token.json', 'w') as token:
          token.write(creds.to_json())

     service = build('gmail', 'v1', credentials=creds)# build GMAIL API service

     # Call the Gmail API to fetch INBOX messages
     results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()

     # Get the messages from the results
     messages = results.get('messages', [])

     if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages[:1]:  # Process 1 message FOR TESTING
               # Get the message from its id
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            # Get the message snippet
            msg_snippet = msg['snippet']
            print(f'Processing message snippet: {msg_snippet}')
            process_content(msg_snippet)


if __name__ == '__main__':
     fetch_mail()
