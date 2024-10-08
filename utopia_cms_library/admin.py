import admin_thumbnails

from martor.models import MartorField

from django.conf import settings
from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.models import Article
from core.admin import UtopiaCmsAdminMartorWidget

from utopia_cms_library.models import (
    BookAuthor,
    BookPublisher,
    BookCategory,
    Book,
    BooksNewsletter,
    BooksNewsletterBlock,
    BooksNewsletterBlockContent,
    BooksNewsletterBlockRow,
)


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(BookPublisher)
class BookPublisherAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_editable = ("name", )


class BookArticleInline(admin.TabularInline):
    model = Book.articles.through
    extra = 3
    max_num = 3
    raw_id_fields = ("article", )
    verbose_name_plural = _("related articles")


@admin.register(Book)
@admin_thumbnails.thumbnail("cover_photo", _("cover photo"), append=False)
class BookAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__name", "categories__name")
    list_display = ("id", "title", "get_authors", "year", "publisher", "cover_photo_thumbnail", "get_articles")
    list_filter = ("authors", "publisher", "categories")
    exclude = ("articles", ) + (
        ("cover_photo_mobile", ) if getattr(settings, "UTOPIA_CMS_LIBRARY_EXCLUDE_COVER_PHOTO_MOBILE", False) else ()
    )
    inlines = [BookArticleInline]
    formfield_overrides = {MartorField: {"widget": UtopiaCmsAdminMartorWidget}}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "articles":
            kwargs["queryset"] = Article.published.all()
        return super(BookAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    class Media:
        css = {'all': ('css/admin_book.css', )}


class BooksNewsletterForm(ModelForm):

    class Meta:
        widgets = {"subject": TextInput(attrs={"size": 140}), "title": TextInput(attrs={"size": 140})}


class BooksNewsletterBlockForm(ModelForm):

    class Meta:
        fields = ["order", "title", "content", "footer"]
        model = BooksNewsletterBlock
        widgets = {"order": TextInput(attrs={"size": 2})}


class BooksNewsletterBlockInline(admin.TabularInline):
    model = BooksNewsletterBlock
    form = BooksNewsletterBlockForm
    raw_id_fields = ("content", )
    formfield_overrides = {MartorField: {"widget": UtopiaCmsAdminMartorWidget}}


@admin.register(BooksNewsletter)
class BooksNewsletterAdmin(admin.ModelAdmin):
    form = BooksNewsletterForm
    inlines = [BooksNewsletterBlockInline]
    date_hierarchy = "day"
    list_display = ("day", "subject", "title")
    formfield_overrides = {MartorField: {"widget": UtopiaCmsAdminMartorWidget}}

    class Media:
        css = {'all': ('css/admin_booksnewsletter.css', )}


class BooksNewsletterBlockRowForm(ModelForm):

    class Meta:
        fields = ["order", "book", "text_content"]
        model = BooksNewsletterBlockRow
        widgets = {"order": TextInput(attrs={"size": 2})}


class BooksNewsletterBlockRowInline(admin.TabularInline):
    model = BooksNewsletterBlockContent.books.through
    form = BooksNewsletterBlockRowForm
    formfield_overrides = {MartorField: {"widget": UtopiaCmsAdminMartorWidget}}
    raw_id_fields = ("book", )


@admin.register(BooksNewsletterBlockContent)
class BooksNewsletterBlockContentAdmin(admin.ModelAdmin):
    inlines = [BooksNewsletterBlockRowInline]
    list_display = ("id", "get_books", "get_blocks")

    class Media:
        css = {'all': ('css/admin_booksnewsletterblockcontent.css', )}
