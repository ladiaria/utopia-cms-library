from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UtopiaCmsLibraryConfig(AppConfig):
    name = "utopia_cms_library"
    verbose_name = _("library")
    SEARCH_ELASTIC_INDEX_NAME = "utopia_cms_library"  # Name of the Elasticsearch index
