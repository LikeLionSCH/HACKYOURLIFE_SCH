from django.urls import path, include
from . import views

urlpatterns = [
    path('gallery/', views.gallery_main, name="gallery_main"),
    path('gallery/board/<str:generation>/', views.gallery_board, name="gallery_board"),
    path('gallery/board/detail/<str:generation>/<str:keyword>', views.gallery_detail, name="gallery_detail"),
    # path('gallery/board/detail/idea', views.gallery_idea_detail, name="gallery_idea_detail"),
    # path('gallery/board/detail/hacka', views.gallery_hacka_detail, name="gallery_hacka_detail"),
    # path('gallery/board/detail/session', views.gallery_session_detail, name="gallery_session_detail"),
    # path('gallery/board/detail/other', views.gallery_other_detail, name="gallery_other_detail"),
    path('gallery/board/create/<str:generation>', views.gallery_create, name="gallery_create"),
    path('gallery/delete/<str:gallery_id>/',views.gallery_delete,name='gallery_delete'),
    path('gallery/update/<str:gallery_id>/',views.gallery_update,name='gallery_update'),
]