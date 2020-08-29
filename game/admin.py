from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import Album, Board, Picture

@admin.register(Album)
# class OrderAdmin(DefaultUserAdmin):
class OrderAdmin(admin.ModelAdmin):

    list_display = ('album_id', 'name', 'created','number_of_images',)
    search_fields = ('name','')
    ordering = ('-created',)

    # fields = ( 
    #     'created', 'updated','new_message',
    # )

    list_filter = (
        'number_of_images','user',
    )
    # readonly_fields = (
    #     'order_id', 'created', 'updated',
    # )

admin.site.register(Board)
admin.site.register(Picture)
