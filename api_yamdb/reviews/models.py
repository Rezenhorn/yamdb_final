from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class CategoriesGenresModel(models.Model):
    name = models.CharField(max_length=settings.NAME_MAX_LENGTH,
                            verbose_name='Название')
    slug = models.SlugField(
        unique=True,
        max_length=settings.SLUG_MAX_LENGTH,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Categories(CategoriesGenresModel):

    class Meta(CategoriesGenresModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(CategoriesGenresModel):

    class Meta(CategoriesGenresModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    name = models.CharField(max_length=settings.NAME_MAX_LENGTH,
                            verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        db_index=True,
        validators=[validate_year],
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Жанр и произведение'
        verbose_name_plural = 'Жанры и произведениея'

    def __str__(self):
        return f"Произведение: {self.title}, Жанр: {self.genre}"


class Feedback(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Review(Feedback):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, message='Минимальное значение рейтинга 1'),
            MaxValueValidator(10, message='Максимальное значение рейтинга 10')
        ]
    )

    class Meta(Feedback.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(Feedback):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(Feedback.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
