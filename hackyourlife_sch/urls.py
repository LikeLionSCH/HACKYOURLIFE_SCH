"""hackyourlife_sch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (handler403, handler404, handler500)

import main

urlpatterns = [
    path('', include('main.urls')),
    path('about/', include('about.urls')),
    path('assignment/', include('assignments.urls')),
    path('', include('notice.urls')),
    path('activity/', include('activity.urls')),
    path('', include('session.urls')),
    path('report/',include('reports.urls')),
    path('', include('google_calendar.urls')),
    path('', include('gallery.urls')),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handler for Custom Error Page Config
handler403 = "main.views.error_403"
handler404 = "main.views.error_404"
handler500 = "main.views.error_500"