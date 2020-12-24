from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('create/<str:assignment_id>/',views.create_Report_view,name='report_create'),
    path('list/<str:assignment_id>/',views.read_Report_list_view,name='report_list'),
    path('detail/<str:report_id>/',views.get_Report_detail_view,name='report_detail'),
    path('update/<str:report_id>/',views.update_Report_view,name='report_update'),
    path('delete/<str:report_id>/',views.delete_Report,name='report_delete')
]