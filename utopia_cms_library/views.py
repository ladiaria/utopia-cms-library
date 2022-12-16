from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Nested

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
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


def book_list(request):
    # Filter the list by category slug and search query if received in the 'q' and 's' query parameters
    category_slug, search_query, context = request.GET.get('q'), request.GET.get('s', ""), {}

    if category_slug:
        context["book_category_slug"] = category_slug

    if search_query:
        search_query = ''.join(dre.findall(search_query))

    if search_query and len(search_query) > 2:
        context["search_query"] = search_query

        # TODO [WIP]: search using django/elastic(if configured)
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

            try:
                r = s.execute()
                total = r.hits.total.value
                # ES hits cannot be paginated with the same django Paginator class, we need to take the results
                # for the page and simulate the dajngo pagination using a simple range list.
                page_results, matches_query = _page_results(request, s, total, 16, "page"), list(range(total))
            except Exception as exc:
                if settings.DEBUG:
                    print("search error: %s" % exc)
                # TODO: load error in context someway, for example as an error form:
                # search_form.add_error('s', _('Search is not possible at this time.'))
            cont, elastic_search = len(matches_query), True

        else:
            matches_query = Book.objects
            if category_slug:
                matches_query = matches_query.filter(categories__slug=category_slug)
            # TODO: uncomment and fix this lines
            # matches_query = matches_query.filter(get_query(search_query, ['title', ...]))
            # cont = matches_query.count()

    else:
        matches_query = Book.objects
        if category_slug:
            matches_query = matches_query.filter(categories__slug=category_slug)

    # Paginate and keep the query by category (if any) to use it in the paginator links
    # TODO [WIP]: should be migrated like search.views
    pager = _paginate(request, matches_query, 16, "page")
    """
    paginator, page = Paginator(queryset, 16), request.GET.get('page')
    try:
        pager = paginator.page(page)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except (EmptyPage, InvalidPage):
        pager = paginator.page(paginator.num_pages)
    """
    context["pager"] = pager


    return render(request, "utopia_cms_library/book_list.html", context)
