from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.shortcuts import render

from .models import Book


class BookDetail(DetailView):
    model = Book
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_detail_urlname'] = self.request.GET.get('category_detail_urlname')
        return context


def book_list(request):
    # Filter the list by category slug if received in the 'q' query parameter
    queryset, category_slug = Book.objects.all(), request.GET.get('q')
    if category_slug:
        context = {"book_category_slug": category_slug}
        queryset = queryset.filter(categories__slug=category_slug)

    # Paginate and keep the query by category (if any) to use it in the paginator links
    paginator, page = Paginator(queryset, 16), request.GET.get('page')
    try:
        pager = paginator.page(page)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except (EmptyPage, InvalidPage):
        pager = paginator.page(paginator.num_pages)
    context["pager"] = pager

    return render(request, "utopia_cms_library/book_list.html", context)
