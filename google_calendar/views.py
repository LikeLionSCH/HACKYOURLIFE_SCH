from datetime import datetime
from calendar import monthrange

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

        now = datetime.utcnow().isoformat() + 'Z'
        last_day = monthrange(datetime.utcnow().year, datetime.utcnow().month)[1]

        # TODO: full calendar api 사용해서 월 전환될 때마다 캘린더 다시 불러오기
        # 시간이 없다 ㅠ 9기들아 부탁해!!!

        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        end_of_month = datetime.utcnow().replace(day=last_day, hour=23, minute=59, second=59, microsecond=999).isoformat() + 'Z'

        # FIXME: 일단 8기 활동을 전부 표시하는 방식으로 임시방편..
        start_of_month = datetime(2020, 1, 1).isoformat() + 'Z'
        end_of_month = None

        print(start_of_month, end_of_month)

        events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=start_of_month, timeMax=end_of_month, singleEvents=True, orderBy='startTime').execute()
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