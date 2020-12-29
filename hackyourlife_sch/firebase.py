import json
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


def SignInRequiredView(func):
    ''' 로그인 된 사용자만 접근할 수 있도록 하는 Decorator.

    Descriptions:
        반드시 request 인자를 가지는 Django View에 사용해야 합니다.

    Examples:
    ```python
        @SignInRequiredView
        def some_view(request, profile_id, ...):
            if request.method == 'POST':
                # uid of signed in user
                print(request.POST['uid'])
                # use your own POST data
                if 'name' in request.POST:
                    print(request.POST['name'])
            return render(request, 'profile.html')
    ```
    '''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # 유저 인증페이지(verify.html)에서 보낸 값인 경우
        if request.method == 'POST':
            # POST 데이터에 requestCode가 없으면
            if 'requestCode' not in request.POST:
                post = request.POST.dict()
                post.pop('csrfmiddlewaretoken')
                return render(request, 'verify.html', {'path': request.path, 'post': json.dumps(post)})

            # POST 데이터에 requestCode는 있지만, 유저 인증페이지(verify.html)로부터 온 값이 아니면
            if request.POST['requestCode'] != 'verify_sign_in_user_request':
                post = request.POST.dict()
                post.pop('requestCode')
                post.pop('csrfmiddlewaretoken')
                return render(request, 'verify.html', {'path': request.path, 'post': json.dumps(post)})

            # 유저 인증페이지(verify.html)를 거쳤고, 유저가 로그인 되어있으면
            if request.POST['uid'] != '':
                # 해당 POST 데이터를 포함하여 함수 호출
                return func(request, *args, **kwargs)

            # 유저 인증페이지(verify.html)를 거쳤고, 유저가 로그아웃 되어있으면 403 Forbidden 에러페이지로 이동
            return HttpResponse('This page is accessible only signed in user.', status=403)
            
        # 첫 접속인 경우, 유저 로그인 인증 페이지로 이동
        return render(request, 'verify.html', {'path': request.path})
    return wrapper