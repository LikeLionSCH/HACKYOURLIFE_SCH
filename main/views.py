from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

import firebase_admin
from firebase_admin import auth

from hackyourlife_sch.firebase import SignInRequiredView, FirestoreControlView


@FirestoreControlView
def transaction(request, db):
    # 등록된 유저인지 검증
    if request.POST['requestCode'] == 'verify_registered_user_request':
        # 로그인을 시도하는 유저의 이메일과 일치하는 document가 하나 이상이면 로그인 승인
        if db.collection('User').where('email', '==', request.POST['email']).get():
            return JsonResponse({'message': 'Current user is registerd member.'})
        return HttpResponse('Current user is not registerd member.', status=400)


def index(request):
    # 클라이언트 요청 처리
    if request.method == 'POST':
        return transaction(request)

    return render(request, 'main.html')


@SignInRequiredView()
@FirestoreControlView
def mypage(request, db):
    uid = request.POST['uid']
    user = auth.get_user(uid)

    likelion_user = [doc.to_dict() for doc in db.collection('User').where('email', '==', user.email).get()][0]
    generation = str(likelion_user['generation']) + '기'
    permission = '운영진' if likelion_user['permission'] == 'manager' else '멤버' if likelion_user['permission'] == 'member' else ''

    data = {
        'photo': user.photo_url,
        'name': user.display_name,
        'generation': generation,
        'permission': permission,
        'email': user.email,
    }

    return render(request, "mypage.html", data)


def post_upload(request):
    return render(request, 'test.html')


def error_403(request, exception):
    return render(request, "403.html", status=403)


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)

@SignInRequiredView()
@FirestoreControlView
def signin_admission_or_refusal(request):
    if request.method == 'POST':
        # 승인/거절 ajax 받았을 시
        if request.POST['admission'] == 'admission':
            email = request.POST['email']
            generation = request.POST['generation']
            permission = request.POST['permission']
            reqest_user_uid = request.POST['request_user_uid']
            username = request.POST['username']

            request_user = {
                'email':email,
                'generation':generation,
                'permission':permission,
                'reqest_user_uid':reqest_user_uid,
                'username':username,
            }

            db.collection('User').document().set(request_user)
            return JsonResponse({'message':'Admission Complete.'})

        uid = request.POST['uid']

        try:
            user = db.collection('User').where('uid','==',uid).get()
            current_user = user[0].to_dict()
        except google.cloud.exceptions.NotFound:
            print('User not found')

        if current_user['permission'] != 'manager':
            raise PermissionDenied # 권한 없음
        
        # firestore User 컬렉션의 목록을 모두 불러와서 딕셔너리들의 리스트로 저장
        admission_users = db.collection('User').stream()
        admission_list = []
        for i in admission_users:
            admission_list.append(admission_users.to_dict())

        # firebase auth의 user 목록을 불러와 email을 기준으로 User 컬렉션에 없는 리스트 생성
        fb_auth_users = auth.list_users().iterate_all()
        wait_users = []
        for user in fb_auth_users:
            if user.email not in admission_list.values():
                wait_users.append(user)

        return render(request, 'account_manager.html', {'wait_users' : wait_users})