import admin_thumbnails

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from core.models import Article
from utopia_cms_library.models import BookAuthor, BookPublisher, BookCategory, Book


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ("name", )


class BookPublisherAdmin(admin.ModelAdmin):
    list_display = ("name", )


class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )


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

admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookPublisher, BookPublisherAdmin)
admin.site.register(BookCategory, BookCategoryAdmin)
admin.site.register(Book, BookAdmin)
