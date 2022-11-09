from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView

from utopia_cms_library.models import Book


class BookList(ListView):
    model = Book

    def get_queryset(self):
        """ Filter the list by category slug if received in the 'q' query parameter """
        queryset, category_slug = super().get_queryset(), self.request.GET.get('q')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        paginator, page = Paginator(queryset, 16), self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except (EmptyPage, InvalidPage):
            queryset = paginator.page(paginator.num_pages)
        return queryset


class BookDetail(DetailView):
    model = Book
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_detail_urlname'] = self.request.GET.get('category_detail_urlname')
        return context