from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return f"{self.username}"


class Quit(models.Model):
    text = models.TextField(max_length=150, verbose_name="Цитата")
    author = models.CharField(max_length=100, verbose_name="Автор")

    class Meta:
        verbose_name_plural = "Цитати"

    def __str__(self):
        return f'"{self.text}" - {self.author} '
