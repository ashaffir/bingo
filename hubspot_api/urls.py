from django.contrib import admin
from django.urls import path, include

from . import views as hubspot_views
# from .views import UserListView

app_name = 'hubspot_api' 
urlpatterns = [
    #Hubspot
    path('', hubspot_views.hubspot_api, name='hubspot_api'),
]
