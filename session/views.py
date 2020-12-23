from django.shortcuts import render, redirect
from hackyourlife_sch.firebase import initialize_firebase

"""
firebase에 저장된 세션 목록을 불러오는 함수
@param : request
@return : session_list 페이지 반환, 세션 목록 전달
"""
def session_list(request):
    session_db = initialize_firebase()  # firebase 초기화
    
    # firebase 접근
    session_ref = session_db.collection('Session')
    sessions = session_ref.stream()

    session_list = {}   # 세션 목록들 저장할 빈 dict 생성

    # session_list에 firebase의 세션 목록들을 하나씩 저장
    for session in sessions:
        session_list[session.id] = session.to_dict()

    print(session_list) # test code
    
    """
    session을 날짜순으로 정렬하는 코드 필요함
    """
    
    # session_list페이지와 함께 session_list 전달
    return render(request, "session_list.html", {'session_list':session_list})

"""
firebase에 세션을 등록하는 함수
@param : request
@return : session_list 페이지 반환, 세션 목록 전달
"""
def session_create(request):
    # POST 요청일 경우에만 session data create
    if request.method == 'POST':
        # firebase 초기화
        session_db = initialize_firebase()

        # get input form
        title = request.POST['title']
        print(request.POST['session_date'])
        print(type(request.POST['session_date']))
        session_date = request.POST['session_date']
        google_link = request.POST['google_link']
        content = request.POST['content']

        print(title, session_date, google_link, content) # test code

        # firebase의 Session 컬렉션 접근 후 자동으로 새 문서 생성(문서 id는 자동 id값)
        session_ref = session_db.collection('Session').document()

        # firebase에 input form data 저장
        session_ref.set({
            'title': title,

            # 현재는 문자열로 등록되는 상태, timestamp로 등록되게 바꿀 예정
            'session_date': session_date,
            
            'google_link': google_link,
            'content': content,
        })

        return redirect('session_list')
    return render(request, 'session_create.html') # POST 요청이 아니면 create 페이지로