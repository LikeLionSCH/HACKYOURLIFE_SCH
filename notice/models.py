from django.db import models

# Create your models here.

class Notice:
    def __init__(self, contents, date, title, file, filename, image, imagename, author):
        self.contents = contents
        self.date = date
        self.title = title
        self.file = file
        self.filename = filename
        self.image = image
        self.imagename = imagename
        self.author = author
        self.notice_id = None


    def to_dict(self):
        # 딕셔너리 생성
        data = {
            'contents': self.contents,
            'date': self.date,
            'title': self.title,
            'file': self.file,
            'filename': self.filename,
            'image': self.image,
            'imagename': self.imagename,
            'author': self.author
        }

        # 생성된 딕셔너리 반환
        return data

    def from_dict(data, notice_id):
        # 객체 생성
        notice = Notice(data['contents'], data['date'], data['title'], data['file'], data['filename'], data['image'], data['imagename'], data['author'])
        notice.notice_id = notice_id

        # 생성된 객체 반환
        return notice

