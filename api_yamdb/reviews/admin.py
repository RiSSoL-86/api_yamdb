from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Сategory, Genre, Title, Title_genre, Review, Comment


@admin.display(description='Текст')
def trim_field_text(obj):
    return u"%s..." % (obj.text[:150],)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        trim_field_text,
        'score',
        'author',
        'pub_date',
        'title'
    )
    list_editable = ('score', 'author')
    list_filter = ('author', 'score', 'pub_date')
    search_fields = ('author', 'text')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        trim_field_text,
        'author',
        'pub_date',
        'review'
    )
    list_filter = ('author', 'pub_date')
    search_fields = ('text', 'author')


class Title_genreInline(admin.TabularInline):
    """Настройка отображения Жанров в Произведениях."""
    model = Title_genre


class TitleAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Настройка Админки-Произведений + добавление возможности импорта/экспорта
    данных из CSV-файлов в БД из Админки."""
    inlines = (Title_genreInline,)
    list_display = ('name', 'year', 'category', 'get_genres')

    def get_genres(self, obj):
        """Функция для корректного отображения Жанров в list_display."""
        return ' '.join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = 'Жанр'

    search_fields = ('name',)
    list_filter = ('category',)
    empty_value_display = 'Не задано'


class ImportExportAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Добавление возможности импорта/экспорта данных из CSV-файлов
    в БД из Админки."""
    ...


    admin.site.register(Title, TitleAdmin)
admin.site.register(Сategory, ImportExportAdmin)
admin.site.register(Genre, ImportExportAdmin)
admin.site.register(Title_genre, ImportExportAdmin)
