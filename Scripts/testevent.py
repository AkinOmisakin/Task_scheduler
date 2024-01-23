import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pytz

# Define the necessary scopes for the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google_calendar():
    """Authenticate and authorize access to the Google Calendar API."""
    creds = None

    # The file token.json stores the user's access and refresh tokens and is created automatically
    # when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_event():
    """Create an event on the user's Google Calendar."""
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    # Define the event details with pytz time zone
    event = {
        'summary': 'Test Event',
        'description': 'This is a test event created using Python.',
        'start': {
            'dateTime': datetime.datetime(2024, 1, 23, 10, 0, 0, tzinfo=pytz.timezone('Europe/London')).isoformat(),
        },
        'end': {
            'dateTime': datetime.datetime(2024, 1, 23, 12, 0, 0, tzinfo=pytz.timezone('Europe/London')).isoformat(),
        },
    }

    # Calendar ID for the primary calendar of the authenticated user
    calendar_id = 'primary'

    try:
        # Create the event
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

        print(f'Event created: {created_event.get("htmlLink")}')
    except Exception as e:
        print(f'Error creating event: {e}')


if __name__ == '__main__':
    create_event()

    # print("Current Directory:", os.getcwd())
    # print("Files in Current Directory:", os.listdir())

