from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Bingo Matrix'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    
    # AllAuth
    # path('accounts/', include('allauth.urls')),
]
