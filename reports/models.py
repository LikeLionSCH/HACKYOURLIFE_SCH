from django.db import models

# Create your models here.
class Report:
    
    """
    생성자
    @param : 과제 아이디값, 쓴사람 문자열, 컨텐츠 문자열, 깃 레포 주소 문자열, 제출일, 제출 상태
    """
    def __init__(self,assignment_id,author,contents,repository_address,submit_date,submit_status):
        self.assignment_id = assignment_id
        self.author = author
        self.contents = contents
        self.repository_address = repository_address
        self.submit_date = submit_date
        self.submit_status = submit_status
        self.report_id = None

    """
    Report 클래스를 딕셔너리 자료구조로 바꿔주는 메소드
    @param : self
    @return : 딕셔너리로 변환된 클래스의 데이터
    """
    def to_dict(self):

        # 딕셔너리 생성
        data = {
            'assignment_id' : self.assignment_id,
            'author' : self.author,
            'contents' : self.contents,
            'repository_address' : self.repository_address,
            'submit_date' : self.submit_date,
            'submit_status' : self.submit_status,
        }
        
        # 생성된 딕셔너리 반환
        return data

    """
    딕셔너리를 불러와 Report 객체로 바꿔주는 메소드
    @pram : 파이어베이스로부터 불러온 dictionary 데이터, 과제 아이디값
    @return : 딕셔너리 데이터를 통해 만들어진 Report 객체
    """
    def from_dict(data,report_id):

        # 객체 생성
        report = Report(data['assignment_id'],data['author'],data['contents'],data['repository_address'],data['submit_date'],data['submit_status'])
        report.report_id = report_id

        # 생성된 객체 반환
        return report