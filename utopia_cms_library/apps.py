from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UtopiaCmsLibraryConfig(AppConfig):
    name = "utopia_cms_library"
    verbose_name = _("library")
    # call this function path (if any) passing it a Book object and returns the result in Book.get_absolute_url
    BOOK_URL_FUNCTION = None
    SEARCH_ELASTIC_INDEX_NAME = "utopia_cms_library"  # Name of the Elasticsearch index
    SEARCH_ELASTIC_INCLUDE_ID = False  # Override to True if you want to include the Book id in the index
