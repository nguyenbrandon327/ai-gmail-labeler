#################################################################################################
#################################################################################################

# NOTES #
# more than likely, if we are to use one entire list for all entities, better to use a set for lack of duplicates and efficiency
# for more advanced usage, can train a custom pipeline to check for our custom entities
# for now, using the pretrained model for ease of use
# also need to check how connectivity works for account linking and inbox access

#################################################################################################
#################################################################################################

import base64 #for decoding message parts
from pyquery import PyQuery as pquery
import requests
import spacy
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

SCOPES = 
[
    'https://www.googleapis.com/auth/gmail.modify',  # read, modify, and delete
    'https://www.googleapis.com/auth/gmail.labels'   # edit labels
]

#function processes each entity within the document tied to the content, then
# prints the entity and the label associated with it, then adds it to a list
#returns list of all normal pretrained labels
# takes a string (content) as a parameter
def process_content(content):
     allLabels = []
     doc = nlp(content)
     for ent in doc.ents:
          print(ent.text, ent.label_)
          allLabels.append(ent.label_)
     
     print("All labels of ents in doc...")
     return allLabels



# checking function to see if the entity is a single word, if not, need to use matcher
def singleWordCheck(wordInList):
     word = wordInList.split()
     return (len(word) == 1)



#function to process custom rule entities
#userRules variable represents a List of custom rules from user input through add-on
#takes content and userRules as parameters
def process_rule_entities(content, userRules):
     allCustomLabels = []
     doc = nlp(content)
     for rule in userRules:
          for ent in doc.ents:
               if singleWordCheck(ent.text):
                    if ent.text == rule:
                         print(f"Custom rule entity found: {ent.text}")
                         allCustomLabels.append(ent.text)
               else:
                    # implement matching function here
     
     # need to implement matchers for >1 word entity searching
     print("All custom rule entities found...")
     return allCustomLabels




# IMPLEMENT A FUNCTION HERE FOR CHECKING ENTITIES AND CUSTOM ENTITIES AGAINST DATABASE OF REQUESTED ENTITIES AND DESIRED ACTIONS
# ex) Entity: "Internship"-->Action: "Star Mail" - - - - - Entity: "Food Subscription Email"-->Action: "Archive Mail"




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






#################################################################################################
# Main function to run the script #
#################################################################################################
if __name__ == '__main__':
     # one long string to check for entities
     stringToProcess = fetch_mail()
     # went with two separate functions for ease of debugging and testing, can combine later if needed
     allNormalLabels = process_content(stringToProcess)
     allCustomLabels = process_rule_entities(stringToProcess, userRulesInput) # where userRulesInput is a list of inputted custom rules 


