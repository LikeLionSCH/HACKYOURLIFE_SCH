from django.shortcuts import render,redirect

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from hackyourlife_sch.firebase import initialize_firebase

from random import *

"""
과제를 등록해주는 함수 (테스트코드)
"""
def create_Assignment():

    # 파이어베이스 초기화
    assignment_db = initialize_firebase()
    
    doc_ref = assignment_db.collection('Assignment').document('AssignmentDoc')
    # documet 에 random 값 집어 넣어 사용 해야 함

    # 작성할 데이터 => dict
    data = doc_ref.set({
        'author':'이남준',
        'content':'테스트용 데이터베이스 asd입ㅁㄴㅇㅁㄴㅇㅁ니다',
        #'deadline':'2020년 1월 1일 오전 12시 0분 0초 UTC+9',
        #'deadline':'2020-12-18',
        'title':'테스트ㅁㅇㅁㅇ용 제asd목 입니다.',
    })

    print(data)

"""
파이어베이스에서 데이터값을 읽어오는 함수 (테스트 코드)
"""
def read_AssignmentList():

    # 파이어베이스 초기화
    assignment_db = initialize_firebase()

    assignment_ref = assignment_db.collection('Assignment')
    assignments = assignment_ref.stream()

    for assignment in assignments:
        print(assignment)

"""
파이어베이스로 과제 데이터를 생성하는 함수
@param : request
@return : assignment_create 페이지 반환
"""
def create_Assignment_view(request):

    # requset 메소드가 POST 일 경우만
    if( request.method=='POST' ):

        # 파이어베이스 초기화
        db = initialize_firebase()

        # form의 값 받아옴
        author = request.POST['author']
        contents = request.POST['contents']
        deadline = request.POST['deadline']
        title = request.POST['title']

        #print(author,contents,deadline,title)

        # 파이어베이스 Assignment 컬렉션 접근
        # documet 랜덤 문자열로 바꿔줘야함
        doc_ref = db.collection('Assignment').document('random_id')
        # 파이어베이스에 값 저장
        doc_ref.set({
            'author':author,
            'content':contents,
            'deadline':deadline,
            'title':title,
        })

        # redirect
        return redirect('assignment_create')
    
    # POST가 아닐 경우 assignment create 페이지 띄움
    return render(request,'assignment_create.html')


"""
파이어베이스에 저장된 과제 목록을 불러오는 함수
@param : request
@return : assignment_list 페이지 반환, 과제 목록 전달
"""
def read_Assignment_view(request):

    # 파이어 베이스 초기화
    db = initialize_firebase()

    # template 으로 전달해줄 리스트 생성
    assignment_list = []

    # 파이어 베이스 접근
    assignment_ref = db.collection('Assignment')
    assignments = assignment_ref.stream()

    # 값을 읽어와 하나씩 assignment_list 에 담는다
    for assignment in assignments:
        assignment_list.append(assignment)
        print(assignment_list)

    # assignment_list 페이지 띄우고 과제 데이터 전달
    return render(request,'assignment_list.html',{'assignments':assignment_list})


#read_AssignmentList()
#create_Assignment()


