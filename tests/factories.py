from decimal import Decimal

import factory.django
from django.contrib.auth.hashers import make_password

from ads.models import Ad
from categories.models import Category
from users.models import User, Location


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    slug = factory.Sequence(lambda n: f'slug{n}')


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Sequence(lambda n: f'Location{n}')
    lat = factory.Faker('latitude')
    lng = factory.Faker('longitude')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: f'user{n}')
    password = make_password('password')
    role = 'member'
    birth_date = factory.Faker('date_of_birth')
    email = factory.Faker('email')
    location = factory.SubFactory(LocationFactory)

    # Переопределяем метод _create для создания пользователя с существующим объектом Location
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        location = kwargs.pop('location', None)
        if location is not None:
            kwargs['location'] = location
        return super()._create(model_class, *args, **kwargs)


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker("name")
    price = Decimal("50.00")
    description = "Про что забыл разработчик который покрыл код тестами на 99% ? https://coub.com/view/2ywl8t"
    is_published = True
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
