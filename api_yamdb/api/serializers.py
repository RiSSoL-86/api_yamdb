from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review


class GetTitleId:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].parser_context['kwargs']['title_id']


class ReviewSerializers(serializers.ModelSerializer):
    """Сериализатор модели review."""
    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=GetTitleId()
    )

    class Meta:
        model = Review
        fields = (
            '__all__'
        )
        read_only_fields = ('title',)

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
            )
        ]

    def validate_score(self, value):
        if 1 < value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10.'
            )
        return value
