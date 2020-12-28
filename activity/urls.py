from django.urls import path
from . import views

urlpatterns = [
    path('study/', views.study, name="study"),
    path('hackathon/', views.hackathon, name="hackathon"),
    path('ideathon/', views.ideathon, name="ideathon"),
    path('etc/', views.etc, name="etc"),
]