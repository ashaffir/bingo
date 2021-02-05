from django.contrib import admin

from .models import Customer, Plan

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','membership', 'cancel_at_period_end',)
    search_fields = ('user','membership',)
    ordering = ('user',)

admin.site.register(Plan)
