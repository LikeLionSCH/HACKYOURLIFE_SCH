from django.shortcuts import render, redirect

from hackyourlife_sch.firebase import FirestoreControlView, SignInRequiredView
from firebase_admin import firestore
import google

from django.core.paginator import Paginator

from .models import Session

from operator import attrgetter
import datetime

# datetime의 KST 설정
KST = datetime.timezone(datetime.timedelta(hours=9))

""" LIST
firebase에 저장된 세션 목록을 불러오는 함수
@param : request
@return : session_list 페이지 반환, 세션 목록 전달
"""
@SignInRequiredView('session/')
@FirestoreControlView
def session_list(request, db):
    # firebase에 접근해 세션 날짜별로 정렬한 목록을 가져옴
    datas = db.collection('Session').order_by('session_date', direction=firestore.Query.DESCENDING).stream()
    
    session_list = [] # 세션 목록들 저장할 빈 list 생성

    # firebase 내 세션 목록을 클래스를 거쳐 list화
    for data in datas:
        session = Session.from_dict(data.to_dict(), data.id)
        session.session_id = data.id
        session_list.append(session)

    # 페이지 네이터
    paginator = Paginator(session_list,5)
    page = int(request.GET.get('page',1))
    sessions = paginator.get_page(page)

    # 검색 버튼을 눌렀을 경우
    if request.method == 'POST' and 'requestCode' not in request.POST: # TODO: SignInRequired의 post와 겹치지 않게 하는 처리 예시

        # 입력값 불러옴
        keyword = request.POST['keyword']

        filtered_session_list = []

        for session in session_list:

            # assignment의 title이 keyword를 포함하고 있을때만
            if keyword in session.title:
                filtered_session_list.append(session)

        # 페이지 네이터
        paginator = Paginator(filtered_session_list,5)
        page = int(request.GET.get('page',1))
        filtered_sessions = paginator.get_page(page)
        
        # 걸러진 세션들만 전달
        return render(request,'session_list.html',{'session_list':filtered_sessions})
    
    # session_list 페이지와 함께 session_list 전달
    return render(request, "session_list.html", {'session_list':sessions})

""" CREATE
firebase에 세션을 등록하는 함수
@param : request
@return : session_list 페이지 반환, 세션 목록 전달
"""
@FirestoreControlView
def session_create(request, db):
    # POST 요청일 경우에만 session data create
    if request.method == 'POST':
        # get input form
        title = request.POST['title']
        host = request.POST['host']
        print(host) # current user input test code
        session_day = request.POST['session_day'] # session_day : 세션 날짜
        session_time = request.POST['session_time'] # session_time : 세션 시간
        google_link = request.POST['google_link']
        content = request.POST['content']

        print(title, host, session_day, session_time, google_link, content) # test code

        # 입력받은 세션 날짜 슬라이싱
        date = session_day.split('-')
        date_year = int(date[0])
        date_month = int(date[1])
        date_day = int(date[2])

        # 입력받은 세션 시간 슬라이싱
        time = session_time.split(':')
        time_hour = int(time[0])
        time_min = int(time[1])

        session_date = datetime.datetime(date_year, date_month, date_day, time_hour, time_min, tzinfo=KST)

        # input data를 클래스 사용으로 객체화
        new_session = Session(title, host, session_date, google_link, content)

        # firebase의 Session 컬렉션 접근 후 자동으로 새 문서 생성(문서 id는 자동 id값)
        # firebase에 새 객체 저장
        db.collection('Session').document().set(new_session.to_dict())

        return redirect('session_list')

    # POST 요청이 아니면 create 페이지로
    return render(request, 'session_create.html')

""" READ
firebase에 저장된 특정 세션을 불러오는 함수
@param : request, 세션의 ID 값
@return : session_detail.html 반환 , session 객체 전달
"""
@SignInRequiredView('session/')
@FirestoreControlView
def session_detail(request, db, session_id):
    # 매개변수의 session_id를 통해 firebase의 세션 불러옴
    try:
        data = db.collection('Session').document(session_id).get()
    except google.cloud.exceptions.NotFound:
        print('Not Found')
    
    # 불러온 세션을 객체로 변경
    session = Session.from_dict(data.to_dict(), data.id)
    print(data.to_dict())

    # 생성된 세션 모델 반환
    return render(request,'session_detail.html',{'session':session})

""" UPDATE
firebase에 저장된 특정 세션을 수정하는 함수
@param : request, 세션의 ID 값
@return : session_detail로 redirect
"""
@FirestoreControlView
def session_update(request, db, session_id):
    # POST 요청일 경우에만 session data create
    if request.method == 'POST':
        # 매개변수의 session_id를 통해 firebase의 세션 불러옴
        try:
            data = db.collection('Session').document(session_id).get()
        except google.cloud.exceptions.NotFound:
            print('Not Found')
        
        # 불러온 세션을 객체로 변경
        session = Session.from_dict(data.to_dict(), data.id)

        # input form의 datas를 객체에 update
        session.title = request.POST['title']
        session.host = request.POST['host']
        print(session.host) # current user input test code

        session_day = request.POST['session_day']
        session_time = request.POST['session_time']
        
        # 입력받은 세션 날짜 슬라이싱
        date = session_day.split('-')
        date_year = int(date[0])
        date_month = int(date[1])
        date_day = int(date[2])

        # 입력받은 세션 시간 슬라이싱
        time = session_time.split(':')
        time_hour = int(time[0])
        time_min = int(time[1])

        # KST에 맞게 변환 후 객체에 저장
        session_date = datetime.datetime(date_year, date_month, date_day, time_hour, time_min, tzinfo=KST)
        session.session_date = session_date

        session.google_link = request.POST['google_link']
        session.content = request.POST['content']

        # test code
        print(session.title, session.host, session.session_date, session.google_link, session.content)

        # firebase의 해당 id에 맞는 문서에 수정된 객체 저장
        db.collection('Session').document(session.session_id).set(session.to_dict())

        return redirect('session_detail', session_id)
    
    else: # GET 요청일 때(update 페이지 진입 시)
        # 매개변수의 session_id를 통해 firebase의 세션 불러옴
        try:
            data = db.collection('Session').document(session_id).get()
        except google.cloud.exceptions.NotFound:
            print('Not Found')

        print(data.to_dict()) # test code

        # 불러온 세션을 객체로 변경
        session = Session.from_dict(data.to_dict(), data.id)

        # UTC -> KST로 변경(firebase에서 가져온 값은 UTC)
        session.session_date = session.session_date + datetime.timedelta(hours=9)
        
        session_date = session.session_date.strftime('%Y-%m-%d %H:%M')
        session_day = str(session_date).split(" ")[0]
        session_time = str(session_date).split(" ")[1]

        # 해당 객체의 데이터와 함께 update 페이지로 이동
        return render(request, 'session_update.html', {
            'session':session,
            'session_day':session_day,
            'session_time':session_time
            })

""" DELETE
firebase에 저장된 특정 세션을 삭제하는 함수
@param : request, 세션의 ID 값
@return : session_list로 redirect
"""
@FirestoreControlView
def session_delete(request, db, session_id):
    # 매개변수의 session_id를 통해 firebase의 세션 불러와 삭제
    db.collection('Session').document(session_id).delete()

    return redirect('session_list')