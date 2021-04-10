from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name='Название',
        help_text='Название категории объекта')
    slug = models.SlugField(
        unique=True, verbose_name='Метка',
        help_text='Уникальная метка для названия категории объекта')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name='Название',
        help_text='Название жанра объекта')
    slug = models.SlugField(
        unique=True, verbose_name='Метка',
        help_text='Уникальная метка для названия жанра объекта')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название',
        help_text='Название произведения'
        )
    year = models.IntegerField(
        db_index=True, null=True, blank=True,
        verbose_name='Год',
        help_text='Год выпуска'
        )
    description = models.TextField(
        null=True, blank=True,
        verbose_name='Описание',
        help_text='Описание произведения'
        )
    genre = models.ManyToManyField(
        Genre, related_name='genres', blank=True,
        verbose_name='Жанр', help_text='Жанр(ы) произведения'
        )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='categories',
        verbose_name='Категория',
        help_text='Категория произведения'
        )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Название произведения'
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание произведения'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Автор произведения'
    )
    score = models.PositiveSmallIntegerField(
        help_text='Введите оценку от 1 до 10',
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'review date',
        auto_now_add=True,
        help_text='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Рецензия',
        help_text='Рецензия на произведение'
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст рецензии'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор рецензии'
    )
    pub_date = models.DateTimeField(
        'comment date',
        auto_now_add=True,
        help_text='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
