from django.contrib import admin

from .models import Payment, Coupon


@admin.register(Payment)
class Payments(admin.ModelAdmin):
    list_display = ('pk','date', 'user','paid', 'amount')
    search_fields = ('user',)
    ordering = ('-date',)

admin.site.register(Coupon)
