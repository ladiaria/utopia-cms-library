from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UtopiaCmsLibraryConfig(AppConfig):
    name = "utopia_cms_library"
    verbose_name = _("library")
    BOOK_URL_FUNCTION = None  # If function path, Book.get_absolute_url will call with a Book obj and return the result
