from django.db import models

# Create your models here.

"""
세션 클래스
"""
class Session:

    session_id = None

    """
    생성자
    @param : self, 세션 제목, 진행자, 진행일자, 구글독스 링크, 내용 문자열
    """
    def __init__(self, title, host, session_date, google_link, content):
        self.title = title
        self.host = host
        self.session_date = session_date
        self.google_link = google_link
        self.content = content

    """
    Session 클래스를 딕셔너리 자료구조로 바꿔주는 메소드
    @param : self
    @return : 딕셔너리로 변환된 클래스의 데이터
    """
    def to_dict(self):
        data = {
            'title':self.title,
            'host':self.host,
            'session_date':self.session_date,
            'google_link':self.google_link,
            'content':self.content,
        }
        
        return data

    """
    딕셔너리를 불러와 Session 객체로 바꿔주는 메소드
    @pram : firebase로부터 불러온 dictionary 데이터
    @return : 딕셔너리 데이터를 통해 만들어진 Session 객체
    """
    def from_dict(data, session_id):
        session = Session(data['title'], data['host'], data['session_date'], data['google_link'], data['content'])
        session.session_id = session_id
        return session