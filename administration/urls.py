from django.urls import path, include

from . import views as views_administration
app_name = 'administration'

urlpatterns = [
    path('', views_administration.admin_home, name='admin_home'),
    path('public_albums', views_administration.public_albums, name='public_albums'),
]
