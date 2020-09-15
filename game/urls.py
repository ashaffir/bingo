from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import (albums,public_albums, pictures, UserAlbumsView, game_room, game_control, 
                    players, game_create, game_request,game_confirm, game_play)

router = routers.DefaultRouter()
# router.register('albums', UserAlbumsView, basename='game')

app_name = 'game'
urlpatterns = [
    path('', include(router.urls)),
    path('albums/', albums, name='albums'),
    path('public-albums/', public_albums, name='public-albums'),
    path('pictures/', pictures, name='pictures'),
    path('game-control/', game_control, name='game-control'),
    path('game-create/', game_create, name='game-create'),
    path('game-request/', game_request, name='game-request'),
    path('game-confirm/', game_confirm, name='game-confirm'),
    path('game-play/', game_play, name='game-play'),
    path('<str:game_id>/', game_room, name='game-room'),
    path('players/<str:user_id>/<str:game_id>/', players, name='players'),

]
