from django.urls import path, re_path
from django.contrib.sitemaps.views import sitemap

from .views import book_list, BookDetail
from .sitemaps import BookSitemap


urlpatterns = [
    path('', book_list, name="library-home"),
    re_path(r'^(?P<slug>[-\w]+)/$', BookDetail.as_view(), name="library-book-detail"),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': {"book": BookSitemap}}, name='library-book-sitemap'),
]
