from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UtopiaCmsLibraryConfig(AppConfig):
    name = "utopia_cms_library"
    verbose_name = _("library")
    BOOK_URL_FUNCTION = None  # If function path, Book.get_absolute_url will call with a Book obj and return the result
    BOOK_LIST_TEMPLATE = "utopia_cms_library/book_list.html"
    SEARCH_ELASTIC_INDEX_NAME = "utopia_cms_library"  # Name of the Elasticsearch index
    SEARCH_ELASTIC_INCLUDE_ID = False  # Override to True if you want to include the Book id in the index
