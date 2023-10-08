from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_yamdb.settings import REGEX_SIGNS, REGEX_ME
from reviews.models import User, Title, Category, Genre, Review, Comment


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class NotAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей не являющихся Админом."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        required=True,
        validators=(REGEX_SIGNS, REGEX_ME)
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    class Meta:
        model = User
        fields = ('email', 'username')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категория."""
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанр."""
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Произведение."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    rating = serializers.SerializerMethodField()

    def to_representation(self, instance):
        """Преобразование отображаемых данных."""
        return TitleSerializerGet().to_representation(instance)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerGet(serializers.ModelSerializer):
    """Сериализатор для метода GET модели Произведение."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        """Получение средней оценки пользователей на произведение."""
        rating = obj.reviews.aggregate(Avg("score")).get("score__avg")
        if not rating:
            return rating
        return round(rating, 2)

    class Meta:
        model = Title
        fields = '__all__'


class GetTitleId:
    """Получение title для ReviewSerializers/title."""
    requires_context = True

    def __call__(self, serializer_field):
        return (serializer_field.context['request']
                .parser_context['kwargs']['title_id'])


class ReviewSerializers(serializers.ModelSerializer):
    """Сериализатор модели review."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=GetTitleId()
    )

    class Meta:
        model = Review
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Вы уже оценили это произведение.'
            )
        ]

    def to_representation(self, instance):
        """Преобразование отображаемых данных."""
        ret = super().to_representation(instance)
        del ret['title']
        return ret


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели comment."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
