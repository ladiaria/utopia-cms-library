from django.conf.urls import url

from .views import book_list, BookDetail


urlpatterns = [
    url(r'^$', book_list, name="library-home"),
    url(r'^(?P<slug>[-\w]+)/$', BookDetail.as_view()),
]
