from django.shortcuts import render

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

"""
파이어베이스 초기화 해주는 함수
@return : firestore.client
"""
def initialize_firebase():

    # 파이어베이스 Initialize
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    
    return firestore.client()


"""
과제를 등록해주는 함수
"""
def create_Assignment():

    # 파이어베이스 초기화
    assignment_db = initialize_firebase()
    
    doc_ref = assignment_db.collection('Assignment').document('AssignmentDoc')

    # 작성할 데이터 => dict
    data = doc_ref.set({
        'author':'이남준',
        'content':'테스트용 데이터베이스 asd입ㅁㄴㅇㅁㄴㅇㅁ니다',
        'deadline':'2020년 1월 1일 오전 12시 0분 0초 UTC+9',
        'title':'테스트ㅁㅇㅁㅇ용 제asd목 입니다.',
    })

    print(data)

"""
파이어베이스에서 데이터값을 읽어오는 함수
"""
def read_AssignmentList():

    # 파이어베이스 초기화
    assignment_db = initialize_firebase()

    assignment_ref = assignment_db.collection('Assignment')
    assignments = assignment_ref.stream()

    for assignment in assignments:
        print(assignment)


read_AssignmentList()
#create_Assignment()


