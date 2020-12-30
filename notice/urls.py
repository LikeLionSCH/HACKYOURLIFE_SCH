from django.urls import path, include
from . import views

urlpatterns = [
    path('notice/', views.notice_list, name="notice_list"),
    path('notice/detail/<str:notice_id>', views.notice_detail, name="notice_detail"),
    #path('notice/detail', views.notice_detail, name="notice_detail"), # 페이지 preview용
    path('faq/', views.faq, name="faq"),
    path('notice/create/', views.notice_create, name="notice_create"),
    path('notice/delete/<str:notice_id>/',views.notice_delete,name='notice_delete'),
    path('notice/update/<str:notice_id>/',views.notice_update,name='notice_update'),
]
