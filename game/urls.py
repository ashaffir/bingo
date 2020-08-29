from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import albums, pictures, UserAlbumsView

router = routers.DefaultRouter()
# router.register('albums', UserAlbumsView, basename='game')

app_name = 'game'
urlpatterns = [
    path('', include(router.urls)),
    path('albums/', albums, name='albums'),
    path('pictures/', pictures, name='pictures'),

]
