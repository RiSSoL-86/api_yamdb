from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Сategory, Genre, Title, Title_genre


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
