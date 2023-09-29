from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from rest_framework import filters


from reviews.models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly, IsAdminOrReadOnlyTitles
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Категория"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Жанр"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Произведение"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnlyTitles,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name', 'year', 'genre', 'category')
