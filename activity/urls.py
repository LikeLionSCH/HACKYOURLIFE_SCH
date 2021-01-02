from django.urls import path
from . import views

urlpatterns = [
    path('activity/study/', views.study, name="study"),
    path('activity/hackathon/', views.hackathon, name="hackathon"),
    path('activity/ideathon/', views.ideathon, name="ideathon"),
    path('activity/etc/', views.etc, name="etc"),
]