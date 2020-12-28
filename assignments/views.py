from django.shortcuts import render,redirect

from django.core.paginator import Paginator

import firebase_admin
import google
from firebase_admin import credentials
from firebase_admin import firestore

from hackyourlife_sch.firebase import FirestoreControlView
from .models import Assignment


"""
파이어베이스로 과제 데이터를 생성하는 함수
@param : request
@return : assignment_create 페이지 반환
"""
@FirestoreControlView
def create_Assignment_view(request, db):

    # request 메소드가 POST 일 경우만
    if( request.method=='POST' ):

        # form의 값 받아오는 코드
        # author = request.POST['author']
        contents = request.POST['contents']
        deadline_date = request.POST['deadline_date']
        deadline_time = request.POST['deadline_time']
        title = request.POST['title']

        deadline = format(deadline_date + ' ' + deadline_time)

        # 과제 객체 생성
        new_assignment = Assignment(firestore.SERVER_TIMESTAMP,"author",contents,deadline,title)

        # firebase 에 데이터 생성
        db.collection('Assignment').document().set(new_assignment.to_dict())

        # redirect
        return redirect('assignment_list')
    
    # POST가 아닐 경우 assignment create 페이지 띄움
    return render(request,'assignment_create.html')


"""
파이어베이스에 저장된 과제 목록을 불러오는 함수
@param : request
@return : assignment_list 페이지 반환, 과제 목록 전달
"""
@FirestoreControlView
def read_Assignment_list_view(request, db):

    # session 에 저장된 uid 값 가져오기
    # uid = request.session['uid']
    # print('assignment list')
    # print(uid)
    # 과제 객체 목록

    # 과제 객체 목록
    assignment_list = []

    # firebase 에 접근해 과제 목록들을 timestamp 기준 내림차순으로 정렬하여 불러옴
    assignment_datas = db.collection('Assignment').order_by('timestamp',direction=firestore.Query.DESCENDING).stream()

    # 값을 읽어와 하나씩 assignment_list 에 담는다
    for assignment_data in assignment_datas:
        assignment = Assignment.from_dict(assignment_data.to_dict(),assignment_data.id)
        assignment_list.append(assignment)

    # 페이지 네이터
    paginator = Paginator(assignment_list,5)
    page = int(request.GET.get('page',1))
    assignments = paginator.get_page(page)

    # 검색 버튼을 눌렀을 경우
    if request.method == 'POST':

        # 입력값 불러옴
        keyword = request.POST['keyword']

        filtered_assignment_list = []

        for assignment in assignment_list:

            # assignment의 title이 ketword를 포함하고 있을때만
            if keyword in assignment.title:
                filtered_assignment_list.append(assignment)

        # 페이지 네이터
        paginator = Paginator(filtered_assignment_list,5)
        page = int(request.GET.get('page',1))
        filtered_assignments = paginator.get_page(page)
        
        # 걸러진 과제들만 전달
        return render(request,'assignment_list.html',{'assignments':filtered_assignments})

    # assignment_list 페이지 띄우고 과제 데이터 전달
    return render(request,'assignment_list.html',{'assignments':assignments})


"""
과제 모델 디테일 뷰
@param : request, 과제의 문자열 아이디값
@return : assignment_deta.html 반환 , assignment 객체 전달
"""
@FirestoreControlView
def get_Assignment_detail_view(request, db, assignment_id):
    # 매개변수의 assignment_id 를 통해 파이어베이스의 과제 불러옴
    try:
        assignment_data = db.collection('Assignment').document(assignment_id).get()
    except google.cloud.exeption.NotFound:
        print('Not Found')
    
    # 불러온 과제를 객체로 변경
    assignment = Assignment.from_dict(assignment_data.to_dict(),assignment_data.id)

    # 위에서 생성된 과제 모델 반환
    return render(request,'assignment_detail.html',{'assignment':assignment})


"""
과제 삭제 함수
@param : request, 과제의 문자열 아이디값
@return : assignment_list로 리다이렉트
"""
@FirestoreControlView
def delete_Assignment(requset, db, assignment_id):
    # 매개변수의 과제 id 로 데이터를 불러와 삭제
    db.collection('Assignment').document(assignment_id).delete()

    # 리스트 뷰로 리다이렉트
    return redirect('assignment_list')


"""
과제 모델 수정하는 함수
@param : request, 등록된 과제의 아이디값
@return : render, redirect
"""
@FirestoreControlView
def update_Assignment_view(request, db, assignment_id):
    # 매개변수의 과제 아이디값으로 파이어베이스에서 과제 데이터 불러오는 코드
    try:
        assignment_data = db.collection('Assignment').document(assignment_id).get()
    except google.cloud.exeption.NotFound:
        print('Not Found')
    
    # 불러온 데이터로 객체 생성
    assignment = Assignment.from_dict(assignment_data.to_dict(),assignment_data.id)

    # 리퀘스트 method 가 POST 일 경우
    if( request.method == 'POST' ):

        # from 으로 부터 입력받은 값 불러오는 코드
        # author = request.POST['author']
        contents = request.POST['contents']
        deadline = request.POST['deadline']
        title = request.POST['title']

        # 파이어베이스에 접속하여 입력된 값으로 수정
        db.collection('Assignment').document(assignment_id).update({
            'author' : "author",
            'contents' : contents,
            'deadline' : deadline,
            'title' : title,
        })

        # 수정 된 과제 디테일 뷰로 리다이렉트
        return redirect('assignment_detail',assignment_id)
    
    # POST 가 아닐 경우 update 창 띄워줌
    return render(request,'assignment_update.html',{'assignment':assignment})
