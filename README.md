This is a draft of a project revolving around the GMAIL API, accessing a user's mail inbox and sort through emails, categorizing and/or
deleting them based on keywords that are found through a custom-created natural language processing model based on named entity
recognition.

1. Access the user's inbox
2. Run it through program to sort into categories (labels in Gmail)
3. Emphasize certain categories based on user input
4. Delete certain categories (uncaught spam, junk one time emails, repetitive, unnecessary mail)
5. Save to inbox

Tools used:
Python (script and NER model will be written in Python)
SpaCy (natural language processing library to create NER model)
GMAIL API (to access user inbox)
Google OAuth2.0 (to allow user sign in for data use)

Dependencies used: (pip install)
spacy google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# ai-gmail-labeler
