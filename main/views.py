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


@SignInRequiredView
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


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)