from django.urls import path
from . import views

urlpatterns = [
    path('about/about/', views.about, name="about"),
    path('about/history/', views.history, name="history"),
    path('about/staff/', views.staff, name="staff"),
    path('about/developer/', views.developer, name="developer"),
]