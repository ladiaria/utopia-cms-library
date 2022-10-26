from django.template import Library, loader

from utopia_cms_library.models import Book


register = Library()


@register.simple_tag()
def book_list():
    return loader.render_to_string('utopia_cms_library/book_list.html', {"object_list": Book.objects.all()})
