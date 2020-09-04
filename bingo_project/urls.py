from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'Bingo Matrix'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/', include('payments.urls', namespace='payments')),
    path('api/', include('api.urls', namespace='api')),
    path('game/', include('game.urls', namespace='game')),
    path('api/users/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
    # AllAuth
    # path('accounts/', include('allauth.urls')),

]
