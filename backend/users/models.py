from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=settings.LENGTH_EMAIL,
        unique=True,
        verbose_name='Электронная почта',
        blank=False
    )
    username = models.CharField(
        max_length=settings.LENGTH_USERNAME,
        verbose_name='Юзернейм',
        unique=True
    )
    first_name = models.CharField(
        max_length=settings.LENGTH_FIRST_NAME,
        verbose_name='Имя',
        blank=False
    )
    last_name = models.CharField(
        max_length=settings.LENGTH_LAST_NAME,
        verbose_name='Фамилия',
        blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
