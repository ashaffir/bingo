from django.contrib import admin

from .models import User
# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('pk','username', 'name', 'phone','balance',)
    search_fields = ('name','username',)
    ordering = ('-name',)

    # fields = ( 
    #     'created', 'updated','new_message',
    # )

    list_filter = (
        'name','balance',
    )
