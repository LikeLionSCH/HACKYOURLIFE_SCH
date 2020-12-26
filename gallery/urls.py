from django.urls import path, include
from . import views

urlpatterns = [
    path('gallery/', views.gallery_main, name="gallery_main"),
    path('gallery/board', views.gallery_board, name="gallery_board"),
    path('gallery/board/detail', views.gallery_detail, name="gallery_detail"),
    path('gallery/board/create', views.gallery_create, name="gallery_create"),
]