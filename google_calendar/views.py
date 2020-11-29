# django modules
from django.shortcuts import render

import datetime
import pickle

# google auth modules
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# google calendar permission: read only
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# calendar view
def calendar(request):
    credentials = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    service = build('calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return render(request, 'calendar.html')

    start_times = []
    summaries = []
    for event in events:
        start_times.append(event['start'].get('dateTime', event['start'].get('date')))
        summaries.append(event['summary'])

    return render(request, 'calendar.html', {'start_times': start_times, 'summaries': summaries})