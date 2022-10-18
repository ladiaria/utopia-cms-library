from django.db import models
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

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(_("title"), max_length=255, unique=True)
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
