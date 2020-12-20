from django.urls import path, include

from . import views as views_administration
app_name = 'administration'

urlpatterns = [
    path('', views_administration.admin_home, name='admin_home'),
]
