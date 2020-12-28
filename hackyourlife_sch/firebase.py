from functools import wraps

from django.shortcuts import render, HttpResponse

import firebase_admin
from firebase_admin import credentials, firestore


def FirestoreControlView(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if not firebase_admin._apps:
            _credentials = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(_credentials)
        return func(request, firestore.client(), *args, **kwargs)
    return wrap


def SignInRequiredView(path):
    def wrapper(func):
        @wraps(func)
        def is_verify_request(request):
            return request.method == 'POST' and 'requestCode' in request.POST and request.POST['requestCode'] == 'verify_sign_in_user_request'

        def decorator(request, *args, **kwargs):
            if is_verify_request(request):
                if request.POST['uid'] != '':
                    return func(request, *args, **kwargs)
                return HttpResponse('This page is accessible only signed in user.', status=500)
            return render(request, 'verify.html', {'path': path})
        return decorator
    return wrapper