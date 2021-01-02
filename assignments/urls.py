from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('assignment/create/',views.create_Assignment_view, name='assignment_create'),
    path('assignment/list/',views.read_Assignment_list_view, name='assignment_list'),
    path('assignment/detail/<str:assignment_id>/',views.get_Assignment_detail_view,name='assignment_detail'),
    path('assignment/delete/<str:assignment_id>/',views.delete_Assignment,name='assignment_delete'),
    path('assignment/update/<str:assignment_id>/',views.update_Assignment_view,name='assignment_update'),
]