from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=settings.LENGTH_USERNAME,
        verbose_name='Юзернейм',
        unique=True
    )
    email = models.EmailField(
        max_length=settings.LENGTH_EMAIL,
        verbose_name='Электронная почта',
        blank=False
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

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


User = get_user_model()
