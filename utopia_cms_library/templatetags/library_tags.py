from django.template import Library, loader

from ..apps import UtopiaCmsLibraryConfig as library_settings
from ..views import search


register = Library()


@register.simple_tag(takes_context=True)
def book_list(context, category_slug, search_query, page, ordering):
    search_query, page_results, pager, error = search(search_query, category_slug, page, ordering)
    context.update(
        {
            "search_query": search_query,
            "page_results": page_results,
            "pager": pager,
            "pager_object_list": getattr(pager, "object_list", []),
            "error": error,
        }
    )
    return loader.render_to_string(library_settings.BOOK_LIST_TEMPLATE, context.flatten())
