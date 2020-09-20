from django.contrib import admin
from .models import Control

@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ('name', 'value_integer','value_float',)
    search_fields = ('name',)

