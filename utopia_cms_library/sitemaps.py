from django.conf import settings
from django.contrib.sitemaps import Sitemap

from .models import Book


class BookSitemap(Sitemap):
    changefreq = 'never'
    priority = 1.0
    protocol = settings.URL_SCHEME

    def items(self):
        return Book.objects.all()
