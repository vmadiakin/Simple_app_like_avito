from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from tests.factories import UserFactory, CategoryFactory


class AdCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()  # Создаем пользователя
        self.category = CategoryFactory()  # Создаем категорию

    def test_ad_create(self):
        # Входные данные для создания объявления
        data = {
            "name": "Название объявления",
            "price": "100.00",
            "description": "Описание объявления",
            "is_published": False,
            "author_id": self.user.id,
            "category_id": self.category.id
        }

        # Отправляем POST-запрос для создания объявления
        response = self.client.post('/ad/create/', data)

        # Проверяем, что ответ имеет статус 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что объявление создано с правильными данными
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['price'], data['price'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['is_published'], data['is_published'])
        self.assertEqual(response.data['author'], self.user.username)
        self.assertEqual(response.data['category'], self.category.name)
