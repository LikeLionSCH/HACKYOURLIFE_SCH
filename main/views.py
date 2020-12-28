from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from hackyourlife_sch.firebase import FirestoreControlView


@FirestoreControlView
def transaction(request, db):
    # 계정 상태 변경: 로그인
    if request.POST['requestCode'] == 'user_signed_in_request':
        # TODO
        return JsonResponse({'message': 'User signed in.'})

    # 계정 상태 변경: 로그아웃
    elif request.POST['requestCode'] == 'user_signed_out_request':
        # TODO
        return JsonResponse({'message': 'User signed out.'})

    # 등록된 유저인지 검증
    elif request.POST['requestCode'] == 'verify_sign_in_user_request':
        # 로그인을 시도하는 유저의 이메일과 일치하는 document가 하나 이상이면 로그인 승인
        if db.collection('User').where('email', '==', request.POST['email']).get():
            return JsonResponse({'message': 'Current user is verified member.'})
        return HttpResponse('Current user is not verified member.', status=400)


def index(request):
    # 클라이언트 요청 처리
    if request.method == 'POST':
        return transaction(request)

    # 로그인이 되었을때 uid 값을 ajax로부터 가져와 session에 저장
    # 다른 페이지에서도 request.session['uid'] 로 뽑아내면 uid 값 사용 가능 => 예시 = assignment_list
    # 문제점 1 : 로그아웃 해도 uid 값이 그대로 남아있음
    # 문제점 2 : 메인 페이지가 아닌 다른 페이지 에서는 안됨
    if request.POST.get('uid'):
        uid = request.POST.get('uid')
        request.session['uid'] = uid
        print(uid)

    # print('main uid')

    return render(request, 'main.html')


def post_upload(request):
    return render(request, 'test.html')

def error_404(request, exception):
    return render(request, "404.html", status=404)

def error_500(request):
    return render(request, "500.html", status=500)