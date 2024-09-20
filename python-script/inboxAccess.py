#function fetches the mail from the user's inbox, then processes the content

import base64 #for decoding message parts
from pyquery import PyQuery as pquery
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

SCOPES = 
[
    'https://www.googleapis.com/auth/gmail.modify',  # read, modify, and delete
    'https://www.googleapis.com/auth/gmail.labels'   # edit labels
]

def fetch_mail():
     creds = None #need to implement credentials for user access later
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
                
               #payload, which contains entire message
               #parts, which contains the message parts in plain and html text

               allMessageParts = ""

               for part in msg['payload']['parts']:
                    msg_snippet = ""
                    textForDecode = part['body']['data']

                    if part['mimeType'] == 'text/plain':
                         decodedText = base64.urlsafe_b64decode(textForDecode).decode('utf-8').strip()
                         msg_snippet = decodedText

                    elif part['mimeType'] == 'text/html':
                         decodedHTML = base64.urlsafe_b64decode(textForDecode).decode('utf-8') # decodes into readable HTML
                         htmlDoc = pquery(decodedHTML) # parses the HTML using PyQuery
                         htmlContent = htmlDoc('.content .text').text() # extracts the only content/text from HTML file
                         msg_snippet = htmlContent.strip()

                    allMessageParts += msg_snippet #concatenates all message parts for processing

               print("Returning message parts...")
               return allMessageParts