from django.contrib import admin
from .models import ContactUs, ContentPage

@admin.register(ContentPage)
class ContentPage(admin.ModelAdmin):
    list_display = ('name','title', 'section','active','language',)
    search_fields = ('name','section',)
    ordering = ('name',)


@admin.register(ContactUs)
class ContactUs(admin.ModelAdmin):
    list_display = ('created','email',)
    search_fields = ('email',)
    ordering = ('-created',)

