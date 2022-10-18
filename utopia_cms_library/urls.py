from django.conf.urls import url
from utopia_cms_library.views import BookList


urlpatterns = [
    url(r'^$', BookList.as_view()),
]
