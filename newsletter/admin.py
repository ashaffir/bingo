from django.contrib import admin
from .models import Newsletter

@admin.register(Newsletter)
class ContactUs(admin.ModelAdmin):
    list_display = ('created','name', 'subject','sent', 'sent_date','recipients_count',)
    search_fields = ('name',)
    ordering = ('-created',)