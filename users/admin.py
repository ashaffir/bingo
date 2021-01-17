from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import User
# admin.site.register(User)
@admin.register(User)
class UserAdmin(ImportExportModelAdmin):

    list_display = ('pk', 'email', 'name', 'phone', 'balance','spent','country','joined',)
    search_fields = ('name', 'username',)
    ordering = ('-name',)

    list_filter = (
        'name', 'balance',
    )
