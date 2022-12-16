from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.template import Library, loader

from utopia_cms_library.models import Book


register = Library()


@register.simple_tag(takes_context=True)
def book_list(context, category_slug, search_query, page, ordering):
    object_list = Book.objects.filter(categories__slug=category_slug) if category_slug else Book.objects.all()
    if search_query:
        # TODO: search using django/elastic(if configured)
        pass
    if ordering:
        object_list = object_list.order_by(ordering)
    paginator = Paginator(object_list, 16)
    try:
        pager = paginator.page(page)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except (EmptyPage, InvalidPage):
        pager = paginator.page(paginator.num_pages)
    context.update({"pager": pager})
    return loader.render_to_string('utopia_cms_library/book_list.html', context.flatten())
