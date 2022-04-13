from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

UserModel = get_user_model()


class MovieDB(models.Model):
    MOVIE_NAME_MAX_CHAR = 100
    GENRES_MAX_CHAR = 100
    ACTORS_MAX_CHAR = 1000
    ROLES_MAX_CHAR = 1000
    PRODUCTION_COMPANIES_MAX_CHAR = 100
    LANGUAGE_MAX_CHAR = 10
    STATUS_MAX_CHAR = 100

    movie_id = models.IntegerField(
        unique=True
    )

    name = models.CharField(
        max_length=MOVIE_NAME_MAX_CHAR
    )

    poster = models.URLField(

    )

    description = models.TextField(

    )

    duration = models.IntegerField(

    )

    genres = models.CharField(
        max_length=GENRES_MAX_CHAR
    )

    average_grade = models.FloatField(

    )

    actors = models.CharField(
        max_length=ACTORS_MAX_CHAR
    )

    roles = models.CharField(
        max_length=ROLES_MAX_CHAR
    )

    production_companies = models.CharField(
        max_length=PRODUCTION_COMPANIES_MAX_CHAR
    )

    language = models.CharField(
        max_length=LANGUAGE_MAX_CHAR
    )

    imdb_link = models.URLField(

    )

    budget = models.FloatField(

    )

    release_date = models.DateField(

    )

    status = models.CharField(
        max_length=STATUS_MAX_CHAR
    )

    def __str__(self):
        return self.name


class List(models.Model):
    LIST_TITLE_MAX_CHAR = 30

    title = models.CharField(
        max_length=LIST_TITLE_MAX_CHAR
    )

    cover = models.URLField(
        blank=True,
        null=True,
        verbose_name='URL Field'

    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (('title', 'user'),)

    def __str__(self):
        return self.title


class Movie(models.Model):
    MOVIE_NAME_MAX_CHAR = 50
    MOVIE_NAME_MIN_CHAR = 2

    GRADE_MAX_CHAR = 10
    GRADE_CHOICE = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )

    RELEASE_DATE_MAX_CHAR = 15

    movie_id = models.IntegerField(

    )

    movie_name = models.CharField(
        max_length=MOVIE_NAME_MAX_CHAR,
        validators=[
            MinLengthValidator(MOVIE_NAME_MIN_CHAR)
        ]
    )

    grade = models.IntegerField(
        choices=GRADE_CHOICE

    )

    would_recommend = models.BooleanField(
        default=True,
        blank=True,
        null=True,
    )

    selected_list = models.ForeignKey(
        List, on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('movie_id', 'selected_list')

    def __str__(self):
        return f'{self.movie_name}'
