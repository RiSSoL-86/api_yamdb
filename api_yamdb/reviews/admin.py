from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import User, Category, Genre, Title, TitleGenre, Review, Comment


@admin.display(description='Текст')
def trim_field_text(obj):
    """Отображаемый текст не превышает 150 символов."""
    return f"{obj.text[:150]}..."


@admin.display(description='Комментариев')
def comment_count(obj):
    """Количество комментариев в отзыве."""
    return obj.comments.count()


@admin.display(description='Отзывов')
def review_count(obj):
    """Количество отзывов в произведение."""
    return obj.reviews.count()


class ImportExportAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Добавление возможности импорта/экспорта данных из CSV-файлов
    в БД из Админки."""
    ...


class ReviewAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Настройка Админки-Отзывов + добавление возможности импорта/экспорта
    данных из CSV-файлов в БД из Админки."""
    list_display = (
        'id',
        trim_field_text,
        'score',
        'author',
        'title',
        'pub_date',
        comment_count
    )
    list_filter = ('pub_date',)
    search_fields = ('title__name', 'text')
    ordering = ('-pub_date',)


class CommentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Настройка Админки-Комментариев + добавление возможности импорта/экспорта
    данных из CSV-файлов в БД из Админки."""
    list_display = (
        'id',
        trim_field_text,
        'author',
        'review',
        'pub_date',
    )
    list_filter = ('pub_date',)
    search_fields = ('text',)
    ordering = ('-pub_date',)


class TitleGenreInline(admin.TabularInline):
    """Настройка отображения Жанров в Произведениях."""
    model = TitleGenre


class TitleAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Настройка Админки-Произведений + добавление возможности импорта/экспорта
    данных из CSV-файлов в БД из Админки."""

    @admin.display(description='Жанр')
    def get_genres(self, obj):
        """Функция для корректного отображения Жанров в list_display."""
        return ' '.join([genre.name for genre in obj.genre.all()])

    inlines = (TitleGenreInline,)
    list_display = (
        'id',
        'name',
        'year',
        'category',
        'get_genres',
        review_count
    )
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
