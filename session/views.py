from django.shortcuts import render
from hackyourlife_sch.firebase import initialize_firebase

"""
파이어베이스에 저장된 세션 목록을 불러오는 함수
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

    #print(session_list) # test code

    # session_list페이지와 함께 session_list 전달
    return render(request, "session_list.html", {'session_list':session_list})