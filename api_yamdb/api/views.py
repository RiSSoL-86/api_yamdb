from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from .serializers import CommentSerializer
from reviews.models import (
    Review, Comment, Title, User
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('reviews_id')
        print(review_id)
        print(title_id)
        return get_object_or_404(
            Review,
            pk=review_id,
            title__id=title_id
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            review=review,
            author=self.request.user
        )
