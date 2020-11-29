# django modules
from django.shortcuts import render
from django.http import HttpResponse

import datetime

# google auth modules
from googleapiclient.discovery import build

# shared calendar id
CALENDAR_ID = 'schlikelion2020@gmail.com'
# google calendar api key
API_KEY = 'AIzaSyCTqmmO5-26iFUs0RWgGvaKjMSpvXqrv08'
# google calendar permission: read only
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# calendar view
def calendar(request):
    service = build('calendar', 'v3', developerKey=API_KEY)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return render(request, 'calendar.html')

    data = []
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        summary = event['summary']
        data.append((start_time, summary))

    return render(request, 'calendar.html', {'data': data})