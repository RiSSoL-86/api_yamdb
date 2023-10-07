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
from .utils import generation_confirmation_code, send_mail_confirmation_code


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
        if request.method != 'PATCH':
            return Response(serializer.data)
        if request.user.is_admin:
            serializer = UsersSerializer(
                request.user,
                data=request.data,
                partial=True)
        else:

            serializer = NotAdminSerializer(
                request.user,
                data=request.data,
                partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthViewSet(viewsets.GenericViewSet):
    @action(
        methods=['POST'],
        detail=False,
        url_path=r'token')
    def get_token(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=(AllowAny,),
        url_path=r'signup')
    def signup(self, request):
        user = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        )
        if not user:
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            confirmation_code = generation_confirmation_code()
            user = serializer.save(
                confirmation_code=confirmation_code
            )
            send_mail_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        send_mail_confirmation_code(user[0])
        return Response(
            'Код подтверждения выслан повторно.',
            status=status.HTTP_200_OK
        )


class CategoryViewSet(viewsets.GenericViewSet,
                      viewsets.mixins.CreateModelMixin,
                      viewsets.mixins.ListModelMixin,
                      viewsets.mixins.DestroyModelMixin):
    """Вьюсет для модели Категория."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.GenericViewSet,
                   viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.ListModelMixin,
                   viewsets.mixins.DestroyModelMixin):
    """Вьюсет для модели Жанр."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Произведение."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGet
        return self.serializer_class


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
