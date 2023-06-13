from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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


def validate_minimum_age(value):
    today = date.today()
    minimum_age_date = today.replace(year=today.year - 9)
    if value > minimum_age_date:
        raise ValidationError('Пользователь должен быть старше 9 лет.')


def validate_email_domain(value):
    if value.endswith('@rambler.ru'):
        raise ValidationError("Регистрация с адреса в домене rambler.ru запрещена.")


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE = [(MEMBER, "Участник"), (MODERATOR, "Модератор"), (ADMIN, "Администратор")]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, validators=[validate_email_domain])
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE, default=MEMBER)
    birth_date = models.DateField(validators=[validate_minimum_age])
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
