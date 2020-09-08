from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import albums, pictures, UserAlbumsView, game_room, game_control, players

router = routers.DefaultRouter()
# router.register('albums', UserAlbumsView, basename='game')

app_name = 'game'
urlpatterns = [
    path('', include(router.urls)),
    path('albums/', albums, name='albums'),
    path('pictures/', pictures, name='pictures'),
    path('game-control/', game_control, name='game-control'),
    path('<str:game_id>/', game_room, name='game-room'),
    path('players/<str:user_id>/<str:game_id>/', players, name='players'),

]
