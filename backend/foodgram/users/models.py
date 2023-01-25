from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    is_subscribed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
