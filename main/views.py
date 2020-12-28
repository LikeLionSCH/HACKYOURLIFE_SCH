from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from hackyourlife_sch.firebase import FirestoreControlView

@FirestoreControlView
def index(request, db):
    # if request.method == 'POST':
    #     # firebase initialize
    #     # user = Firebase.instance().get_current_user()

    #     email = request.POST['userEmail']
    #     print('email address:', email) # test code
    #     domain = email.split('@')[-1]
    #     print('email domain:', domain) # test code
    #     if domain == "likelion.org":
    #         user = auth.get_user(request.POST['uid'])
    #         data = {'name': user.display_name, 'photo': user.photo_url}
    #         print(data)
    #         return render(request, 'main.html', data)
    #     else:
    #         return redirect('main')
    if request.method == 'POST':
        # 등록된 유저인지 검증
        if request.POST['requestCode'] == 'verify_sign_in_user_request':
            # 로그인을 시도하는 유저의 이메일과 일치하는 document가 하나 이상이면 로그인 승인
            if db.collection('User').where('email', '==', request.POST['email']).get():
                response = {'message': 'Current user is verified member.'}
                return JsonResponse(response)
            return HttpResponse('Current user is not verified member.', status=403)


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