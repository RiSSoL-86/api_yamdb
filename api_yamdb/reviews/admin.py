from django.contrib import admin

from .models import (
    Review,
    Comment
)


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
    list_editable = (
        'score',
        'author',
    )
    list_filter = (
        'author',
        'score',
        'pub_date',
    )
    search_fields = (
        'author',
        'text',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        trim_field_text,
        'author',
        'pub_date',
        'review'
    )
    list_filter = (
        'author',
        'pub_date',
    )
    search_fields = (
        'text',
        'author',
    )
