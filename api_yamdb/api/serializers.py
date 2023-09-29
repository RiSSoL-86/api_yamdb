from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Title, Category, Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категория"""
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанр"""
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Произведение"""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        """Получение средней оценки пользователей на произведение"""
        return round(obj.reviews.aggregate(Avg("score")).get("score__avg"), 1)

    class Meta:
        model = Title
        fields = '__all__'
