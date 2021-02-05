from django.urls import path
from django.urls.conf import include

from . import views

app_name = 'newsletter'

urlpatterns = [
    path('newsletter_admin/', views.newsletter_admin, name='newsletter_admin'),
    path('unsubscribe/<str:user_id>', views.unsubscribe, name='unsubscribe'),
    path('newsletter_test/', views.newsletter_test, name='newsletter_test'),
    path('newsletter_form/', views.newsletter_form, name='newsletter_form'),
    path('re_subscribe/<str:user_id>/', views.re_subscribe, name='re_subscribe'),
    path('landing_page/', views.landing_page, name='landing_page'),
]