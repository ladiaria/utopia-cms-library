from __future__ import unicode_literals

from builtins import object

from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from models import Book


@registry.register_document
class BookDocument(Document):
    class Index(object):
        # Name of the Elasticsearch index (TODO: use a better default name, for example "utopiacms_core_article")
        name = getattr(settings, "SEARCH_ELASTIC_ARTICLES_INDEX_NAME", 'books')
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    publisher = fields.TextField(attr="publisher_index")
    authors = fields.TextField(attr="get_authors")
    categories = fields.TextField(attr="get_categories")
    description = fields.TextField(attr="description")

    class Django(object):
        model = Book  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
        ]

        # To ignore auto updating of Elasticsearch index when a model is saved or deleted, use:
        # ignore_signals = True

        # To don't perform an index refresh after every update (overrides global setting), use:
        # auto_refresh = False

        # To paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting), use this example line:
        # queryset_pagination = 5000
