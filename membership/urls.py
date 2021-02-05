from django.contrib import admin
from django.urls import path, include
from membership import views

app_name = 'membership'

urlpatterns = [
    path('', views.plans, name='plans'),
    path('join/', views.join, name='join'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('membership_settings/', views.membership_settings, name='membership_settings'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('updateaccounts/', views.updateaccounts, name='updateaccounts'),
]