from rest_framework import serializers

from reviews.models import Review, Title, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        read_only_fields = ('review',)
