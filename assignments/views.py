from django.shortcuts import render,redirect

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from hackyourlife_sch.firebase import initialize_firebase

"""
과제 클래스
"""
class Assignment():

    """
    생성자
    @param : self, 작성자 문자열, 컨탠츠 문자열, 마감일자 문자열, 제목 문자열
    """
    def __init__(self,author,contents,deadline,title):
        self.author = author
        self.contents = contents
        self.deadline = deadline
        self.title = title

    """
    Assignment 클래스를 딕셔너리 자료구조로 바꿔주는 메소드
    @param : self
    @return : 딕셔너리로 변환된 클래스의 데이터
    """
    def to_dict(self):
        data = {
            'author':self.author,
            'contents':self.contents,
            'deadline':self.deadline,
            'title':self.title,
        }
        
        return data


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


