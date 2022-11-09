from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.template import Library, loader

from utopia_cms_library.models import Book


register = Library()


@register.simple_tag(takes_context=True)
def book_list(context, category_slug, page):
    object_list = Book.objects.filter(categories__slug=category_slug) if category_slug else Book.objects.all()
    paginator = Paginator(object_list, 16)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except (EmptyPage, InvalidPage):
        object_list = paginator.page(paginator.num_pages)
    context.update({"object_list": object_list})
    return loader.render_to_string('utopia_cms_library/book_list.html', context.flatten())
