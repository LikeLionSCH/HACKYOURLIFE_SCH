from django.db import models

# Create your models here.
"""
과제 클래스
"""
class Assignment:

    """
    생성자
    @param : self, 작성자 문자열, 컨탠츠 문자열, 마감일자 문자열, 제목 문자열
    """
    def __init__(self,author,contents,deadline,title):
        self.author = author
        self.contents = contents
        self.deadline = deadline
        self.title = title
        self.assignment_id = None

    """
    Assignment 클래스를 딕셔너리 자료구조로 바꿔주는 메소드
    @param : self
    @return : 딕셔너리로 변환된 클래스의 데이터
    """
    def to_dict(self):

        # 딕셔너리 생성
        data = {
            'author':self.author,
            'contents':self.contents,
            'deadline':self.deadline,
            'title':self.title,
        }
        
        # 생성된 딕셔너리 반환
        return data

    """
    딕셔너리를 불러와 Assignment 객체로 바꿔주는 메소드
    @pram : 파이어베이스로부터 불러온 dictionary 데이터, 과제 아이디값
    @return : 딕셔너리 데이터를 통해 만들어진 Assignment 객체
    """
    def from_dict(data,assignment_id):

        # 객체 생성
        assignment = Assignment(data['author'],data['contents'],data['deadline'],data['title'])
        assignment.assignment_id = assignment_id

        # 생성된 객체 반환
        return assignment