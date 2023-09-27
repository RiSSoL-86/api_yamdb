from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from .serializers import ReviewSerializers
from reviews.models import (
    Review, Comment, Title, User
)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    pagination_class = LimitOffsetPagination

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(
            Title,
            pk=title_id
        )

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            title=title,
            author=self.request.user
        )
