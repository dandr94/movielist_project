from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from movielist_web_project.accounts.managers import MovieListUserManager
from movielist_web_project.web.helpers.validators import validate_only_letters


class MovieListUser(AbstractBaseUser, PermissionsMixin):
    EMAIL_UNIQUE_ERROR_MESSAGE = 'This email is already in use.'

    email = models.EmailField(
        error_messages={'required': EMAIL_UNIQUE_ERROR_MESSAGE},
        unique=True,
        null=False,
        blank=False

    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_superuser = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'

    objects = MovieListUserManager()


class Profile(models.Model):
    USERNAME_MAX_CHAR = 15

    FIRST_NAME_MAX_CHAR = 15
    FIRST_NAME_MIN_CHAR = 2

    LAST_NAME_MAX_CHAR = 15
    LAST_NAME_MIN_CHAR = 2

    username = models.CharField(
        max_length=USERNAME_MAX_CHAR,
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_CHAR,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(FIRST_NAME_MIN_CHAR),
            validate_only_letters
        ]

    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_CHAR,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(LAST_NAME_MIN_CHAR),
            validate_only_letters
        ]
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    twitter = models.URLField(
        blank=True,
        null=True,
    )

    instagram = models.URLField(
        blank=True,
        null=True,
    )

    facebook = models.URLField(
        blank=True,
        null=True,
    )

    user = models.OneToOneField(MovieListUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.username
