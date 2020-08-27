from django.urls import path, include
from users import views

app_name = 'users'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register/', views.registration_view, name='register'),

    # Restrict acccess to logged in users only
    path('restricted/', views.restricted, name='restricted'),

]