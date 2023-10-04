from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]

REGEX_SIGNS = RegexValidator(r'^[\w.@+-]+\Z', 'Поддерживаемые знаки.')
REGEX_ME = RegexValidator(r'[^m][^e]', 'Имя пользователя не может быть "me".')


class User(AbstractUser):
    """Модель Пользователя."""
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=(REGEX_SIGNS, REGEX_ME),
        verbose_name='Никнейм пользователя',
        help_text='Укажите никнейм пользователя'
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='E-mail пользователя',
        help_text='Укажите e-mail пользователя'
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
        max_length=64,
        verbose_name='Роль пользователя',
        help_text='Укажите роль пользователя'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография пользователя',
        help_text='Укажите биографию пользователя'
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Укажите имя пользователя'
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Фамилия пользователя',
        help_text='Укажите фамилия пользователя'
    )
    confirmation_code = models.CharField(
        null=True,
        max_length=64,
        default='XXXX',
        verbose_name='Код подтверждения пользователя',
        help_text='Укажите код подтверждения пользователя'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категорий."""
    name = models.TextField(
        max_length=256,
        verbose_name='Тип произведения',
        help_text='Укажите тип произведения',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Тег',
        help_text='Укажите Тег категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.TextField(
        max_length=256,
        verbose_name='Жанр произведения',
        help_text='Укажите жанр произведения',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Тег',
        help_text='Укажите Тег жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.TextField(
        max_length=256,
        verbose_name='Название произведения',
        help_text='Укажите название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год издания',
        help_text='Укажите год выпуска произведения'
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание произведения",
        help_text='Добавьте описание к произведению'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Тип произведения',
        help_text='Укажите тип произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        through='TitleGenre',
        related_name='titles',
        verbose_name='Жанр произведения',
    )

    class Meta:
        ordering = ["-year"]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Вспомогательная модель: Произведение - Жанр."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titlegenres',
        verbose_name='Название произведения',
        help_text='Укажите название произведения'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titlegenres',
        verbose_name='Жанр произведения',
        help_text='Укажите жанр к произведению'
    )

    class Meta:
        verbose_name = 'Произведение - Жанр'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title} - {self.genre}"


class Review(models.Model):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Укажите произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Добавьте описание отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Укажите автора'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=10,
                message='Оценка больше 10.'
            ),
            MinValueValidator(
                limit_value=1,
                message='Оценка меньше 1.'
            )
        ],
        verbose_name='Оценка',
        help_text='Оцените произведение, в диапазоне от 1 до 10'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_review'
        )]

    def __str__(self):
        return f"{self.title} - {self.author}"


class Comment(models.Model):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Укажите отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Добавьте описание комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Укажите автора'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"{self.review} - {self.author}"
