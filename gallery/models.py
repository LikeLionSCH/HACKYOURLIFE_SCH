from django.db import models

# Create your models here.
"""
갤러 클래스
"""

class Gallery:
    def __init__(self, contents, created_at, title, image_url, place,):
        self.contents = contents
        self.created_at = created_at
        self.title = title
        self.image_url = image_url
        self.place = place
        self.gallery_id = None

    def to_dict(self):
        # 딕셔너리 생성
        data = {
            'contents': self.contents,
            'created_at': self.created_at,
            'title': self.title,
            'image_url': self.image_url,
            'place': self.place,
        }

        # 생성된 딕셔너리 반환
        return data

    def from_dict(data, gallery_id):
        # 객체 생성
        gallery = Gallery(data['image_url'], data['contents'], data['created_at'], data['title'], data['place'],)
        gallery.gallery_id = gallery_id

        # 생성된 객체 반환
        return gallery
