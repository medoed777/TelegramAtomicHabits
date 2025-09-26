from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите почту", blank=False, null=False)
    phone = models.CharField(max_length=15, verbose_name="Телефон", help_text="Введите номер телефона")
    city = models.CharField(max_length=50, verbose_name="Город", help_text="Введите город", blank=True, null=True)
    chat_id = models.CharField(max_length=50, verbose_name="ID номер чата в телеграм")
    avatar = models.ImageField(upload_to="users/avatar", verbose_name="Аватар", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
