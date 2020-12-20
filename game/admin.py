from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from import_export.admin import ImportExportModelAdmin

from .models import Album, Board, Picture, Game, Player


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):

    list_display = ('album_id', 'name', 'created',
                    'number_of_pictures', 'board_size', 'public_approved',)
    search_fields = ('name',)
    ordering = ('-created',)

    # fields = (
    #     'created', 'updated','new_message',
    # )

    list_filter = (
        'user',
    )
    # readonly_fields = (
    #     'order_id', 'created', 'updated',
    # )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'created', 'game_id', 'album_id',
                    'started', 'number_of_players', 'is_finished',)
    search_fields = ('user__email', 'number_of_players', 'game_id',)
    ordering = ('-created',)
    list_filter = ('user', 'number_of_players', )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('game', 'player_id', 'created',
                    'player_game_id', 'nickname', 'approved', 'not_approved',)
    search_fields = ('nickname', 'game__game_id',)
    ordering = ('-created',)


@admin.register(Picture)
class PictureAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name', 'album_id', 'url',)
    search_fields = ['name', 'url', ]
    ordering = ('name',)
    list_filter = ('album_id',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game_id', 'size', 'player',)
    list_filter = ('game_id', 'size',)
    search_fields = ['game_id', 'player__player_id', 'pk', ]
    ordering = ('-created',)


# admin.site.register(Board)
