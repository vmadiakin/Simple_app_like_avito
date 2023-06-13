import pytest
from rest_framework_simplejwt.tokens import AccessToken
from tests.factories import UserFactory


@pytest.fixture
def member_token():
    # Получаем пользователя из фабрики
    user = UserFactory()

    # Генерируем токен доступа для пользователя
    token = AccessToken.for_user(user)

    # Возвращаем токен в виде строки
    return str(token)
