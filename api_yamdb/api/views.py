from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Category, Genre, Title, Review, Comment
from .filters import TitleFilter
from .permissions import (
    AdminOnly, IsAdminOrReadOnly,
    IsAuthorAdminModerOrReadOnly
)
from .serializers import (
    UsersSerializer, NotAdminSerializer, GetTokenSerializer, SignUpSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer, TitleSerializerGet,
    ReviewSerializers, CommentSerializer
)
from .utils import send_mail_confirmation_code


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Пользователя."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'GET':
            return Response(serializer.data)
        if request.user.is_admin:
            serializer = UsersSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
        else:
            serializer = NotAdminSerializer(
                request.user,
                data=request.data,
                partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthViewSet(viewsets.GenericViewSet):
    """Вьюсет для аунтификации Пользователей."""
    @action(
        methods=['POST'],
        detail=False,
        url_path='token')
    def get_token(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if default_token_generator.check_token(
            user,
            data.get('confirmation_code')
        ):
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=(AllowAny,),
        url_path='signup')
    def signup(self, request):
        user = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        )
        if not user:
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail_confirmation_code(user, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        send_mail_confirmation_code(user[0], confirmation_code)
        return Response(
            'Код подтверждения выслан повторно.',
            status=status.HTTP_200_OK
        )


class CategoryGenreMixin(viewsets.GenericViewSet,
                         viewsets.mixins.CreateModelMixin,
                         viewsets.mixins.ListModelMixin,
                         viewsets.mixins.DestroyModelMixin):
    """Миксин для вьюсетов Категории и Жанры"""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreMixin):
    """Вьюсет для модели Категория."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    """Вьюсет для модели Жанр."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Произведение."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    search_fields = ('year',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGet
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet модели Отзывы."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = (IsAuthorAdminModerOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

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


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet модели Комментарии."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModerOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('reviews_id')
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
