from django.template import Library, loader

from utopia_cms_library.models import Book


register = Library()


@register.simple_tag(takes_context=True)
def book_list(context, category_slug):
    context.update(
        {"object_list": Book.objects.filter(categories__slug=category_slug) if category_slug else Book.objects.all()}
    )
    return loader.render_to_string('utopia_cms_library/book_list.html', context.flatten())
