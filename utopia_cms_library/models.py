from autoslug.fields import AutoSlugField
from django_markdown.models import MarkdownField

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import Article

class BookPublisher(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("publisher")
        verbose_name_plural = _("publishers")

    def __str__(self):
        return self.name

class BookAuthor(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __str__(self):
        return self.name

class BookCategory(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)
    slug = AutoSlugField(populate_from="name", always_update=True, null=True, blank=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(_("title"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from="title", always_update=True, null=True, blank=True)
    year = models.PositiveSmallIntegerField(_("year"))
    authors = models.ManyToManyField(BookAuthor, verbose_name=_("authors"))
    publisher = models.ForeignKey(BookPublisher, verbose_name=_("publisher"))
    description = models.TextField(_("description"), blank=True, null=True)
    cover_photo = models.ImageField(_("cover photo"), upload_to="book_covers", blank=True, null=True)
    categories = models.ManyToManyField(BookCategory, verbose_name=_("categories"))
    articles = models.ManyToManyField(Article, verbose_name=_("articles"))

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")

    def get_authors(self):
        return ", ".join(str(a) for a in self.authors.all())
    get_authors.short_description = _("authors")

    def __str__(self):
        return "%s - %s - %s, %d" % (self.title, self.get_authors(), self.publisher, self.year)


class BooksNewsletterBlockRow(models.Model):
    block = models.ForeignKey("BooksNewsletterBlockContent")
    order = models.PositiveSmallIntegerField(_("order"), null=True, blank=True)
    book = models.ForeignKey(Book, verbose_name=_("book"))
    text_content = MarkdownField(_("text content"), blank=True, null=True)

    def __str__(self):
        return str(self.book)

    class Meta:
        verbose_name = _("books newsletter block row")
        verbose_name_plural = _("books newsletter block rows")


class BooksNewsletterBlockContent(models.Model):
    books = models.ManyToManyField(Book, through=BooksNewsletterBlockRow, verbose_name=_("books"))

    def __str__(self):
        return ", ".join(str(book) for book in self.books.all())

    class Meta:
        verbose_name = _("books newsletter block content")
        verbose_name_plural = _("books newsletter block contents")


class BooksNewsletterBlock(models.Model):
    newsletter = models.ForeignKey("BooksNewsletter", related_name=_("blocks"))
    order = models.PositiveSmallIntegerField(_("order"), null=True, blank=True)
    title = models.CharField(_("title"), max_length=255, blank=True, null=True)
    content = models.ForeignKey(BooksNewsletterBlockContent, verbose_name=_("content"))
    footer = MarkdownField(_("footer"), blank=True, null=True)

    def __str__(self):
        return "%s - %d %s" % (self.title or _("no title"), self.content.books.count(), _("books"))

    class Meta:
        verbose_name = _("books newsletter block")
        verbose_name_plural = _("books newsletter blocks")


class BooksNewsletter(models.Model):
    day = models.DateField(_("date"), unique=True, default=timezone.now)
    subject = models.CharField(_("subject"), max_length=255)
    title = models.CharField(_("title"), max_length=255)
    header = MarkdownField(_("header"), blank=True, null=True)
    footer = MarkdownField(_("footer"), blank=True, null=True)

    def __str__(self):
        return "%s: %s" % (self.day, self.title)

    class Meta:
        verbose_name = _("books newsletter")
        verbose_name_plural = _("books newsletters")
        ordering = ("-day", )
        get_latest_by = "day"
