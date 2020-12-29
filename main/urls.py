from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="main"),
    path('mypage/', views.mypage, name="mypage"),
    path('test/', views.post_upload, name="post"),
]
