from django.shortcuts import render, redirect
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from hackyourlife_sch.firebase import initialize_firebase

def index(request):
    if request.method == 'POST':
        # cred = credentials.Certificate('serviceAccountKey.json')
        # firebase_admin.initialize_app(cred)

        # firebase initialize
        db = initialize_firebase()

        email = request.POST['userEmail']
        print('email address:', email) # test code
        domain = email.split('@')[-1]
        print('email domain:', domain) # test code
        if domain == "likelion.org":
            user = auth.get_user(request.POST['uid'])
            data = {'name': user.display_name, 'photo': user.photo_url}
            print(data)
            return render(request, 'main.html', data)
        else:
            return redirect('main')

    data = {'name': 'user', 'photo': 'url'}
    print(data)
    return render(request, 'main.html', data)


def post_upload(request):
    return render(request, 'test.html')