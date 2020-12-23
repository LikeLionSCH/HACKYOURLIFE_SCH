from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('create/',views.create_Assignment_view, name='assignment_create'),
    path('list/',views.read_Assignment_view, name='assignment_list'),
    path('detail/<str:assignment_id>/',views.get_Assignment_detail_view,name='assignment_detail'),
]