from django.contrib import admin
from django.urls import path, include

from . import views as payment_views

app_name = 'payments'
urlpatterns = [
    #Paypal
    path('paypal_return/', payment_views.paypal_return, name='paypal_return'),
    path('paypal_cancel/', payment_views.paypal_cancel, name='paypal_cancel'),
    path('paypal-ipn/', include('paypal.standard.ipn.urls')),
    path('thankyou/', payment_views.payment_success, name='payment_success'),
    path('error/', payment_views.payment_error, name='payment_error'),


    # Paypal
    path('payment/<int:amount>', payment_views.payment, name='payment'),
    # Stripe
    path('charge/', payment_views.charge, name='charge'),
    path('success/<str:args>/', payment_views.successMsg, name="success"),
    path('deposits/', payment_views.deposits, name='deposits'),


]
