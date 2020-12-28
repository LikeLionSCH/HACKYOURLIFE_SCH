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

    return render(request, 'main.html')


def post_upload(request):
    return render(request, 'test.html')