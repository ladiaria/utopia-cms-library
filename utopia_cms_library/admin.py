import admin_thumbnails
from django_markdown.widgets import MarkdownWidget

from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from core.models import Article
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


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ("name", )


class BookPublisherAdmin(admin.ModelAdmin):
    list_display = ("name", )


class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_editable = ("name", )


class BookArticleInline(admin.TabularInline):
    model = Book.articles.through
    extra = 3
    max_num = 3
    raw_id_fields = ("article", )
    verbose_name_plural = _("related articles")


@admin_thumbnails.thumbnail("cover_photo", _("cover photo"), append=False)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "get_authors", "year", "publisher", "cover_photo_thumbnail")
    exclude = ("articles", )
    inlines = [BookArticleInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "articles":
            kwargs["queryset"] = Article.published.all()
        return super(BookAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class BooksNewsletterForm(ModelForm):

    class Meta:
        widgets = {
            "subject": TextInput(attrs={'size': 140}),
            "title": TextInput(attrs={'size': 140}),
            "header": MarkdownWidget(),
            "footer": MarkdownWidget(),
        }


class BooksNewsletterBlockForm(ModelForm):

    class Meta:
        fields = ["order", "title", "content", "footer"]
        model = BooksNewsletterBlock
        widgets = {"order": TextInput(attrs={"size": 3}), "footer": MarkdownWidget()}


class BooksNewsletterBlockInline(admin.TabularInline):
    model = BooksNewsletterBlock
    form = BooksNewsletterBlockForm
    raw_id_fields = ("content", )


class BooksNewsletterAdmin(admin.ModelAdmin):
    form = BooksNewsletterForm
    inlines = [BooksNewsletterBlockInline]  # TODO: improve styles


class BooksNewsletterBlockRowForm(ModelForm):

    class Meta:
        fields = ["order", "book", "text_content"]
        model = BooksNewsletterBlockRow
        widgets = {"order": TextInput(attrs={"size": 3}), "text_content": MarkdownWidget()}


class BooksNewsletterBlockRowInline(admin.TabularInline):
    model = BooksNewsletterBlockContent.books.through
    form = BooksNewsletterBlockRowForm
    raw_id_fields = ("book", )


class BooksNewsletterBlockContentAdmin(admin.ModelAdmin):
    # TODO: improve columns width
    inlines = [BooksNewsletterBlockRowInline]


admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookPublisher, BookPublisherAdmin)
admin.site.register(BookCategory, BookCategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BooksNewsletter, BooksNewsletterAdmin)
admin.site.register(BooksNewsletterBlockContent, BooksNewsletterBlockContentAdmin)
