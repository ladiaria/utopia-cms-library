from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Nested

from django.conf import settings
from django.views.generic import DetailView
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from search.models import get_query
from search.views import dre, _paginate, _page_results

from .models import Book, BookCategory
from .documents import BookDocument

class BookDetail(DetailView):
    model = Book
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_detail_urlname'] = self.request.GET.get('category_detail_urlname')
        return context


def search(search_query, category_slug, page, ordering=""):
    """
    @returns A tuple with 4 items:
             - the sanitized search query
             - the page results (if elastic was used to search)
             - the pager object
             - an error message if any error was detected
    """
    page_results, error = None, ""

    if search_query:
        search_query = ''.join(dre.findall(search_query))

    if search_query and len(search_query) > 2:

        if settings.ELASTICSEARCH_DSL:

            extra_kwargs = {}
            if settings.SEARCH_ELASTIC_MATCH_PHRASE:
                elastic_match_phrase = True
                extra_kwargs['type'] = 'phrase'
            elif settings.SEARCH_ELASTIC_USE_FUZZY:
                extra_kwargs['fuzziness'] = 'auto'

            s = BookDocument.search()
            if category_slug:
                s = s.filter(
                    Nested(
                        path="categories_filter",
                        query=Q("match", categories_filter__name=BookCategory.objects.get(slug=category_slug).name),
                    )
                )
            s = s.query(
                Q(
                    "bool",
                    should=[
                        Q(
                            'multi_match',
                            query=search_query,
                            fields=['title^2', 'year', 'publisher.name', 'description'],
                            **extra_kwargs,
                        ),
                        Nested(path="authors", query=Q("match_bool_prefix", authors__name=search_query)),
                        Nested(path="categories", query=Q("match_bool_prefix", categories__name=search_query)),
                    ],
                )
            )
            if ordering:
                s = s.sort(ordering)
            try:
                r = s.execute()
                total = r.hits.total.value
                # ES hits cannot be paginated with the same django Paginator class, we need to take the results
                # for the page and simulate the dajngo pagination using a simple range list.
                page_results, matches_query = _page_results(page, s, total, 16), list(range(total))
            except Exception as exc:
                if settings.DEBUG:
                    print("search error: %s" % exc)
                matches_query, error = None, _('Search is not possible at this time.')

        else:
            matches_query = Book.objects
            if category_slug:
                matches_query = matches_query.filter(categories__slug=category_slug)
            matches_query = matches_query.filter(
                get_query(
                    search_query,
                    ['title', 'year', 'publisher__name', 'description', 'authors__name', 'categories__name'],
                )
            ).distinct()
            if ordering:
                matches_query = matches_query.order_by(ordering)

    else:
        matches_query = Book.objects.all()
        if category_slug:
            matches_query = matches_query.filter(categories__slug=category_slug)
        if ordering:
            matches_query = matches_query.order_by(ordering)

    return (search_query, page_results, matches_query and _paginate(page, matches_query, 16), error)


def book_list(request):
    # Filter the list by category slug and search query if received in the 'q' and 's' query parameters
    category_slug, search_query, page = request.GET.get('q'), request.GET.get('s', ""), request.GET.get("page")
    context = {"book_category_slug": category_slug} if category_slug else {}
    search_query, page_results, pager, error = search(search_query, category_slug, page)
    context.update({"search_query": search_query, "page_results": page_results, "pager": pager, "error": error})
    return render(request, "utopia_cms_library/book_list.html", context)
