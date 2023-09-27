from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import User, Category, Genre, Title, TitleGenre, Review, Comment


@admin.display(description='Текст')
def trim_field_text(obj):
    """Отображаемый текст не превышает 150 символов."""
    return u"%s..." % (obj.text[:150],)


class ImportExportAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Добавление возможности импорта/экспорта данных из CSV-файлов
    в БД из Админки."""
    ...


class ReviewAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = (
        trim_field_text,
        'score',
        'author',
        'title',
        'pub_date'
    )

    list_editable = ('score', 'author')
    list_filter = ('pub_date',)
    search_fields = ('author',)


class CommentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = (
        trim_field_text,
        'author',
        'review',
        'pub_date'
    )
    list_filter = ('pub_date',)
    search_fields = ('author',)


class TitleGenreInline(admin.TabularInline):
    """Настройка отображения Жанров в Произведениях."""
    model = TitleGenre


class TitleAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Настройка Админки-Произведений + добавление возможности импорта/экспорта
    данных из CSV-файлов в БД из Админки."""
    inlines = (TitleGenreInline,)
    list_display = ('name', 'year', 'category', 'get_genres')

    def get_genres(self, obj):
        """Функция для корректного отображения Жанров в list_display."""
        return ' '.join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = 'Жанр'

    search_fields = ('name',)
    list_filter = ('category',)
    empty_value_display = 'Не задано'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, ImportExportAdmin)
admin.site.register(Category, ImportExportAdmin)
admin.site.register(Genre, ImportExportAdmin)
admin.site.register(TitleGenre, ImportExportAdmin)
