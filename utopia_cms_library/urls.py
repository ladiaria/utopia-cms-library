from django.conf.urls import url
from utopia_cms_library.views import BookList, BookDetail


urlpatterns = [
    url(r'^$', BookList.as_view(), name="library-home"),
    url(r'^(?P<slug>[-\w]+)/$', BookDetail.as_view()),
]
