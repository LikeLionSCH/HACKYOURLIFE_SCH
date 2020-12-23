from django.shortcuts import render,redirect

import firebase_admin
import google
from firebase_admin import credentials
from firebase_admin import firestore

from hackyourlife_sch.firebase import initialize_firebase
from .models import Assignment


"""
파이어베이스로 과제 데이터를 생성하는 함수
@param : request
@return : assignment_create 페이지 반환
"""
def create_Assignment_view(request):

    # request 메소드가 POST 일 경우만
    if( request.method=='POST' ):

        # firebase initialize
        db = initialize_firebase()

        # form의 값 받아오는 코드
        author = request.POST['author']
        contents = request.POST['contents']
        deadline = request.POST['deadline']
        title = request.POST['title']

        # 과제 객체 생성
        new_assignment = Assignment(author,contents,deadline,title)

        # firebase 에 데이터 생성
        db.collection('Assignment').document().set(new_assignment.to_dict())

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

    # firebase initialize
    db = initialize_firebase()

    # template 으로 전달해줄 리스트 생성
    assignments = []

    # firebase 에 접근해 과제 목록들 불러옴
    datas = db.collection('Assignment').stream()

    # 값을 읽어와 하나씩 assignment_list 에 담는다
    for data in datas:
        assignment = Assignment.from_dict(data.to_dict(),data.id)
        assignments.append(assignment)

    # assignment_list 페이지 띄우고 과제 데이터 전달
    return render(request,'assignment_list.html',{'assignments':assignments})


"""
과제 모델 디테일 뷰
@param : request, 과제의 문자열 아이디값
@return : assignment_deta.html 반환 , assignment 객체 전달
"""
def get_Assignment_detail_view(request,assignment_id):

    # firemase initialize
    db = initialize_firebase()

    # 매개변수의 assignment_id 를 통해 파이어베이스의 과제 불러옴
    try:
        data = db.collection('Assignment').document(assignment_id).get()
    except google.cloud.exeption.NotFound:
        print('Not Found')
    
    # 불러온 과제를 객체로 변경
    assignment = data.to_dict()

    # 위에서 생성된 과제 모델 반환
    return render(request,'assignment_detail.html',{'assignment':assignment})


"""
과제 삭제 함수
@param : request, 과제의 문자열 아이디값
@return : assignment_list로 리다이렉트
"""
def delete_Assignment(requset,assignment_id):

    # firebase initialize
    db = initialize_firebase()

    # 매개변수의 과제 id 로 데이터를 불러와 삭제
    db.collection('Assignment').document(assignment_id).delete()

    # 리스트 뷰로 리다이렉트
    return redirect('assignment_list')


def update_Assignment_view(request):
    pass



