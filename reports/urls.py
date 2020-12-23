from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('create/<str:assignment_id>/',views.create_Report_view,name='report_create')
]