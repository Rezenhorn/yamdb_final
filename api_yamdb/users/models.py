from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator


class User(AbstractUser):
    """Кастомная модель юзера."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN)
    )

    username = models.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        validators=(UsernameValidator(),),
        verbose_name='Никнейм пользователя'
    )
    password = models.CharField(
        max_length=settings.PASSWORD_MAX_LENGTH,
        blank=True,
        verbose_name='Пароль'
    )
    email = models.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='Имейл'
    )
    first_name = models.CharField(
        max_length=settings.FIRST_NAME_MAX_LENGTH,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=settings.LAST_NAME_MAX_LENGTH,
        blank=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=max([len(role) for role, _ in ROLE_CHOICES]),
        choices=ROLE_CHOICES,
        default=USER
    )

    @property
    def is_admin(self):
        return (
            self.is_staff or self.is_superuser or self.role == self.ADMIN
        )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
