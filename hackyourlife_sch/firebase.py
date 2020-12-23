import firebase_admin
from firebase_admin import credentials, firestore

"""
파이어베이스 초기화 해주는 함수
@return : firestore.client
"""
def initialize_firebase():
    # serviceAccountKey로 처음 한번만 firebase와 인증/연결되도록 설정
    if not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)

    return firestore.client()