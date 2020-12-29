from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('create/<str:assignment_id>/',views.create_Report_view,name='report_create'),
    path('list/<str:assignment_id>/',views.read_Report_list_view,name='report_list'),
    path('detail/<str:assignment_id>/<str:report_id>/',views.get_Report_detail_view,name='report_detail'),
    path('update/<str:assignment_id>/<str:report_id>/',views.update_Report_view,name='report_update'),
    path('scoring/<str:assignment_id>/<str:report_id>/',views.scoring_Report_view,name='report_scoring'),
    path('delete/<str:assignment_id>/<str:report_id>/',views.delete_Report,name='report_delete'),
    path('my/list/',views.my_report_page,name='my_list'),
]