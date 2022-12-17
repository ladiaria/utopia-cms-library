from django.template import Library, loader

from utopia_cms_library.views import search


register = Library()


@register.simple_tag(takes_context=True)
def book_list(context, category_slug, search_query, page, ordering):
    search_query, page_results, pager, error = search(search_query, category_slug, page, ordering)
    context.update({"search_query": search_query, "page_results": page_results, "pager": pager, "error": error})
    return loader.render_to_string('utopia_cms_library/book_list.html', context.flatten())
