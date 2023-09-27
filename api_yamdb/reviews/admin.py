from django.contrib import admin

from .models import (
    Review,
    Comment
)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'score',
        'author',
        'pub_date',
        'title'
    )
    filter_horizontal = (
        'author',
        'score',
        'pub_date',
        'title'
    )
    search_fields = (
        'text',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'pub_date',
        'review'
    )
    filter_horizontal = (
        'author',
        'pub_date',
        'review'
    )
    search_fields = (
        'text',
    )
