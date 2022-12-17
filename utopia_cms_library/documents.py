from __future__ import unicode_literals

from builtins import object

from django_markup.templatetags.markup_tags import apply_markup

from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .apps import UtopiaCmsLibraryConfig as library_settings
from .models import Book


@registry.register_document
class BookDocument(Document):
    class Index(object):
        name = library_settings.SEARCH_ELASTIC_INDEX_NAME
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    # target searchable fields
    year = fields.TextField(attr="year")
    authors = fields.NestedField(properties={"name": fields.TextField()})
    publisher = fields.ObjectField(properties={"name": fields.TextField()})
    description = fields.TextField(attr="description")
    categories = fields.NestedField(properties={"name": fields.TextField()})
    # field used to match exact name when filtering by category (KeywordField)
    categories_filter = fields.NestedField(attr="categories", properties={"name": fields.KeywordField()})
    # fields used to render the results
    slug = fields.TextField(attr="slug")
    get_authors = fields.TextField(attr="get_authors")

    def prepare_description(self, instance):
        return apply_markup(instance.description, "markdown")

    class Django(object):
        model = Book  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            # target searchable field
            'title',
            # field used to render the results
            'cover_photo',
        ]
        if library_settings.SEARCH_ELASTIC_INCLUDE_ID:
            fields.append('id')

        # To ignore auto updating of Elasticsearch index when a model is saved or deleted, use:
        # ignore_signals = True

        # To don't perform an index refresh after every update (overrides global setting), use:
        # auto_refresh = False

        # To paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting), use this example line:
        # queryset_pagination = 5000
