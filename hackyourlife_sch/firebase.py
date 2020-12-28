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
        def decorator(request, *args, **kwargs):
            if request.method == 'POST' and request.is_ajax():
                if request.POST['uid'] != '':
                    return func(request, *args, **kwargs)
                return HttpResponse('This page is accessible only signed in user.', status=500)
            return render(request, 'verify.html', {'path': path})
        return decorator
    return wrapper