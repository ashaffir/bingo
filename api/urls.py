from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import (check_server,)

# Endpoints list:
# Register: http://127.0.0.1:8010/api/auth/users/
# Login: http://127.0.0.1:8010/api/auth/token/login/
# Logout: http://127.0.0.1:8010/api/auth/token/logout/  - make sure to add token of user to the Headers

router = routers.DefaultRouter(trailing_slash=False)
# router.register('auth', AuthViewSet, basename='auth')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('users.urls')),
    path('check-server/', check_server, name='check-server'),
    path('users/', include('users.urls')),
    path('game/', include('game.urls', namespace='game')),

]
