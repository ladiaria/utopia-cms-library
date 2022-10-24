from django.views.generic import ListView, DetailView

from utopia_cms_library.models import Book


class BookList(ListView):
    model = Book

    def get_queryset(self):
        """ Filter the list by category slug if received in the 'q' query parameter """
        queryset, category_slug = super().get_queryset(), self.request.GET.get('q')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        return queryset


class BookDetail(DetailView):
    model = Book
    query_pk_and_slug = True
