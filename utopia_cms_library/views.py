from django.shortcuts import render
from django.views.generic import ListView

from utopia_cms_library.models import Book


class BookList(ListView):
    # TODO: receive a parameter to filter the list by category (?category=...)
    model = Book
