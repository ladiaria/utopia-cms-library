from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from .views import book_list, BookDetail
from .sitemaps import BookSitemap


urlpatterns = [
    url(r'^$', book_list, name="library-home"),
    url(r'^(?P<slug>[-\w]+)/$', BookDetail.as_view()),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {"book": BookSitemap}}, name='library-book-sitemap'),
]
