from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

class Review(models.Model):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        help_text='Оценка произведения, в диапазоне от 1 до 10',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Сategory(models.Model):
    """Модель категорий."""
    name = models.TextField(verbose_name='Тип произведения',
                            help_text='Укажите тип произведения',
                            max_length=64)
    slug = models.SlugField(verbose_name='Тег',
                            max_length=64,
                            unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.TextField(verbose_name='Жанр произведения',
                            help_text='Укажите жанр произведения',
                            max_length=64)
    slug = models.SlugField(verbose_name='Тег',
                            max_length=64,
                            unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.TextField(verbose_name='Название произведения',
                            help_text='Укажите название произведения',
                            max_length=256)
    year = models.IntegerField(verbose_name='Год издания',
                               help_text='Укажите год выпуска произведения')
    description = models.TextField(
        blank=True,
        verbose_name="Описание произведения",
        help_text='Добавьте описание к произведению'
    )
    category = models.ForeignKey(
        Сategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Тип произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        through='Title_genre',
        blank=True,
        related_name='titles',
        verbose_name='Жанр произведения',
    )

    class Meta:
        ordering = ["-year"]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Title_genre(models.Model):
    """Вспомогательная модель: Произведение - Жанр."""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_genres',
        verbose_name='Название произведения'
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='title_genres',
        verbose_name='Жанр произведения'
    )

    class Meta:
        verbose_name = 'Произведение - Жанр'
        verbose_name_plural = 'Произведение - Жанр'

    def __str__(self):
        return f"{self.title_id} - {self.genre_id}"
