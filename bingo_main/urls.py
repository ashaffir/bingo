from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views as bingo_main_views

app_name = 'bingo_main'

urlpatterns = [
    path('', bingo_main_views.bingo_main, name='bingo_main'),
    path('register', bingo_main_views.bingo_main_register,name='bingo_main_register'),
    path('login/', bingo_main_views.bingo_main_login, name='bingo_main_login'),
    path('logout_view', bingo_main_views.logout_view, name='logout_view'),
    path('contact', bingo_main_views.contact, name='contact'),
    path('terms', bingo_main_views.terms, name='terms'),
    path('privacy', bingo_main_views.privacy, name='privacy'),
    path('pricing', bingo_main_views.pricing, name='pricing'),
    path('why_and_how', bingo_main_views.why_and_how, name='why_and_how'),
    path('about', bingo_main_views.about, name='about'),
    path('update_profile', bingo_main_views.update_profile, name='update_profile'),


    path('dashboard/', bingo_main_views.dashboard, name='dashboard'),
    path('create_bingo/', bingo_main_views.create_bingo, name='create_bingo'),
    path('create_bingo/<str:album_id>',bingo_main_views.create_bingo, name='create_bingo'),
    path('start_bingo/', bingo_main_views.start_bingo, name='start_bingo'),
    path('my_bingos/', bingo_main_views.my_bingos, name='my_bingos'),
    path('instructions/', bingo_main_views.instructions, name='instructions'),
    path('bingo/<str:player_id>', bingo_main_views.bingo, name='bingo'),
    path('add_money/', bingo_main_views.add_money, name='add_money'),
    path('broadcast/', bingo_main_views.broadcast, name='broadcast'),
    path('game/<str:game_id>/', bingo_main_views.game, name='game'),
    path('current_displayed_picture/<str:game_id>/',bingo_main_views.current_displayed_picture, name='current_displayed_picture'),
    path('player_card/<str:game_id>/<str:player_id>/<str:user_id>/',bingo_main_views.player_card, name='player_card'),
    path('player_approval_status/<str:game_id>/<str:player_id>/',bingo_main_views.player_approval_status, name='player_approval_status'),
    path('check_game_id/', bingo_main_views.check_game_id, name='check_game_id'),
    path('check_board/<str:game_id>',bingo_main_views.check_board, name='check_board'),
    path('game_over/<str:game_id>', bingo_main_views.game_over, name='game_over'),
    path('player_approval/<str:player_id>/<str:approval>',bingo_main_views.player_approval, name='player_approval'),
    path('bingo_players_list/<str:game_id>',bingo_main_views.bingo_players_list, name='bingo_players_list'),


    # path('game_status/<str:game_id>', bingo_main_views.game_status, name='game_status'),
    path('players_approval_list/<str:game_id>',bingo_main_views.players_approval_list, name='players_approval_list'),


]
