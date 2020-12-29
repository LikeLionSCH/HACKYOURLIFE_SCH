from functools import wraps

from django.shortcuts import render, HttpResponse

import firebase_admin
from firebase_admin import credentials, firestore


def FirestoreControlView(func):
    ''' 유효한 Firestore client를 매개변수로 전달하는 Decorator.
    
    Descriptions:
        Firestore client를 전달하기 전에 항상 Firebase의 초기화 상태를 검증합니다.

    Examples:
    ```python
        @FirestoreControlView
        def some_view(request, db, ...):
            db.collection('Likelion').document('8th').set({'name': 'Annonymous'})
    ```
    '''
    @wraps(func)
    def wrap(*args, **kwargs):
        # Firebase 초기화
        if not firebase_admin._apps:
            _credentials = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(_credentials)
        # 키워드 매개변수 `db`로 Firestore client 전달
        return func(*args, **kwargs, db=firestore.client())
    return wrap


def SignInRequiredView(path):
    ''' 로그인 된 사용자만 접근할 수 있도록 하는 Decorator.

    Descriptions:
        반드시 request 인자를 가지는 Django View에 사용해야 합니다.
        pk 인자를 갖는 경우, pk 이름에 `id`가 들어가야 합니다. ex) post_id

    Args:
        path (str): pk값을 제외한 url 경로

    Examples:
        url: http://localhost:8000/profile/10
    ```python
        @SignInRequiredView('profile/')
        def some_view(request, profile_id, ...):
            if request.method == 'POST' and 'requestCode' in request.POST:
                # uid of signed in user
                print(request.POST['uid'])
            elif request.method == 'POST' and 'requestCode' not in request.POST:
                # Use your own POST data...
                pass
            return render(request, 'profile.html')
    ```
    '''
    def wrapper(func):
        @wraps(func)
        def is_verify_request(request):
            # POST 데이터의 requestCode가 'verify_sign_in_user_request'이면 True
            return request.method == 'POST' and 'requestCode' in request.POST and request.POST['requestCode'] == 'verify_sign_in_user_request'

        def decorator(request, *args, **kwargs):
            # 유저 인증페이지(verify.html)에서 보낸 값인 경우
            if is_verify_request(request):
                # 유저가 로그인 되어있으면
                if request.POST['uid'] != '':
                    # 해당 POST 데이터를 포함하여 함수 호출
                    return func(request, *args, **kwargs)
                # 유저가 로그아웃 되어있으면 403 Forbidden 에러페이지로 이동
                return HttpResponse('This page is accessible only signed in user.', status=403)

            # pk 값만을 추출
            # 함수가 갖는 전체 키워드 매개변수에서, 키워드 이름에 `id`가 들어가는 변수의 값만 list화 시킨다
            pk = [str(value) + '/' if 'id' in key else None for key, value in kwargs.items()]
            # pk 리스트의 모든 문자열을 이어 붙인다
            # 만약 pk 리스트가 비어있으면 빈 문자열 할당
            pk = ''.join(pk) if pk else ''
            return render(request, 'verify.html', {'path': path + pk})
        return decorator
    return wrapper