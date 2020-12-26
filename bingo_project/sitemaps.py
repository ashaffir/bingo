from django.contrib.sitemaps import Sitemap

from game.models import Game

class GameSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def games(self):
        return Game.objects.all()