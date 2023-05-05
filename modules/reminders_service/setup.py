# Module that manages the creation of credentials and authentication with the Google API
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = "modules/settings/credentials.json"


def get_calendar_service():
    creds = None
    if os.path.exists('modules/data/token.pkl'):
        creds = pickle.load(open('modules/data/token.pkl', 'rb'))
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE, SCOPES
        )
        creds = flow.run_local_server(post=0)
        with open('modules/data/token.pkl', 'wb') as file:
            pickle.dump(creds, file)
    return build('calendar', "v3", credentials=creds)
