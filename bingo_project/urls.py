import platform
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
# from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

from bingo_main import views as bingo_main_views

from game import views as game_views

from django.contrib.sitemaps.views import sitemap
from .sitemaps import GameSitemap

if platform.system() == 'Darwin':  # MAC
    admin.site.site_header = 'PolyBingo-Development'
else:
    admin.site.site_header = 'PolyBingo'

sitemaps = {
    'games':GameSitemap()
}

urlpatterns = [
    # path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='sitemap'),
    path('sitemap.xml', TemplateView.as_view(template_name="bingo_main/sitemap.xml", content_type="text/xml")),
    path("robots.txt", TemplateView.as_view(template_name="bingo_main/robots.txt", content_type="text/plain")),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('administration/', include('administration.urls', namespace='administration')),
    # path('', game_views.home, name='home'),
    path('', include('bingo_main.urls', namespace='home')),
    path('frontend/', include('frontend.urls', namespace='frontend')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('api/', include('api.urls', namespace='api')),
    path('game/', include('game.urls', namespace='game')),
    path('users/', include('users.urls', namespace='users')),
    # path('api/users/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),


    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('password-reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/reset_password.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    # AllAuth
    path('accounts/', include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


handler404 = 'bingo_main.views.handler404'
handler403 = 'bingo_main.views.handler403'
handler500 = 'bingo_main.views.handler500'
