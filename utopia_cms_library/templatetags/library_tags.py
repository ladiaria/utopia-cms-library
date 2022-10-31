from django.template import Library, loader

from utopia_cms_library.models import Book


register = Library()


@register.simple_tag(takes_context=True)
def book_list(context):
    context.update({"object_list": Book.objects.all()})
    return loader.render_to_string('utopia_cms_library/book_list.html', context.flatten())
