from functools import wraps

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
