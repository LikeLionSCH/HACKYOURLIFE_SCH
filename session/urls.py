from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('session/', views.session_list, name="session_list"),
    path('session/create/', views.session_create, name="session_create"),
    path('session/<str:session_id>/', views.session_detail, name="session_detail"),
    #path('session/<str:session_id>/update', views.session_update, name="session_update"),
    path('session/<str:session_id>/delete', views.session_delete, name="session_delete"),
]