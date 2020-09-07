from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from import_export.admin import ImportExportModelAdmin

from .models import Album, Board, Picture, Game, Player

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):

    list_display = ('album_id', 'name', 'created','pictures',)
    search_fields = ('name','')
    ordering = ('-created',)

    # fields = ( 
    #     'created', 'updated','new_message',
    # )

    list_filter = (
        'pictures','user',
    )
    # readonly_fields = (
    #     'order_id', 'created', 'updated',
    # )

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk','created','game_id','album_id', 'user','is_finished',)
    search_fields = ('user',)
    ordering = ('-created',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_id','created','player_game_id', 'nickname',)
    search_fields = ['player_id','nickname','game__game_id','created',]
    ordering = ('-created',)

@admin.register(Picture)
class PictureAdmin(ImportExportModelAdmin):
    list_display = ('name','album', 'url',)
    search_fields = ['name','album','url',]
    ordering = ('name',)    

admin.site.register(Board)
