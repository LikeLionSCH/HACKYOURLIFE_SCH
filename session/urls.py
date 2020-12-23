from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('session/', views.session_list, name="session_list"),
]