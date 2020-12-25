import datetime

# django modules
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from hackyourlife_sch import settings

# google auth modules
from googleapiclient.discovery import build

# shared calendar id
CALENDAR_ID = 'schlikelion2020@gmail.com'
# google calendar api key
API_KEY = settings.get_secret('CALENDAR_API_KEY')
# google calendar permission: read only
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# calendar view
def calendar(request):
    if request.method == 'POST':
        service = build('calendar', 'v3', developerKey=API_KEY)

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        first_of_month = datetime.datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=first_of_month, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        data = []
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            end_time = event['end'].get('dateTime', event['end'].get('date'))
            title = event['summary'] if 'summary' in event else '제목 없음'
            description = event['description'] if 'description' in event else '설명 없음'
            data.append({
                'title': title,
                'description': description,
                'start': start_time,
                'end': end_time
            })

        data = { 'list': data }
        return JsonResponse(data)

    return render(request, 'calendar.html')