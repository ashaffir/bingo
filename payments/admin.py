from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class Payments(admin.ModelAdmin):
    list_display = ('date', 'user','paid', 'amount')
    search_fields = ('user',)
    ordering = ('-date',)

# admin.site.register(Payment)
