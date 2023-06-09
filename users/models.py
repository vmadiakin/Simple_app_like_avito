from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE = [(MEMBER, "Участник"), (MODERATOR, "Модератор"), (ADMIN, "Администратор")]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE, default=MEMBER)
    age = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Selection(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('ads.Ad')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'
