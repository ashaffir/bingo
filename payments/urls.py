from django.contrib import admin
from django.urls import path, include

from . import views as payment_views
# from .views import UserListView

app_name = 'payments'
urlpatterns = [
    #Paypal
    path('paypal_return/', payment_views.paypal_return, name='paypal_return'),
    path('paypal_cancel/', payment_views.paypal_cancel, name='paypal_cancel'),
    path('paypal-ipn/', include('paypal.standard.ipn.urls')),
    path('thankyou/', payment_views.payment_success, name='payment_success'),
    path('error/', payment_views.payment_error, name='payment_error'),


    # Paypal
    # path('payment/<int:amount>', payment_views.payment, name='payment'),
    path('payment/<int:amount>/<str:coupon>/', payment_views.payment, name='payment'),
    path('stripe_payment/<int:amount>', payment_views.stripe_payment, name='stripe_payment'),
    # Stripe
    path('charge/', payment_views.charge, name='charge'),
    path('success/<str:args>/', payment_views.successMsg, name="success"),
    path('deposits/', payment_views.deposits, name='deposits'),

    # path('invoices/', payment_views.render_pdf_view, name='render_pdf_view'),
    # path('users_invoices/', UserListView.as_view(), name='users_invoices'),
    path('pdfs/<pk>/', payment_views.user_render_pdf_view, name='user_render_pdf_view'),
    path('invoice_html/', payment_views.invoice_html, name='invoice_html'),
    


]
