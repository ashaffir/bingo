from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings

from . import views as frontend_views

app_name = 'frontend'
urlpatterns = [
    path('', frontend_views.frontend_index, name='frontend_index'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
