from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name="about"),
    path('history/', views.history, name="history"),
    path('staff/', views.staff, name="staff"),
    path('developer/', views.developer, name="developer"),
]