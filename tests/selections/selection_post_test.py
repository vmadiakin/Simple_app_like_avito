from django.test import TestCase
from django.contrib.auth import get_user_model

from tests.factories import CategoryFactory, UserFactory, AdFactory
from users.models import Selection

User = get_user_model()


class SelectionTestCase(TestCase):
    def setUp(self):
        # Создаем необходимые объекты для теста
        self.category = CategoryFactory()
        self.user = UserFactory()
        self.ad = AdFactory(category=self.category, author=self.user)

    def test_create_selection(self):
        # Создаем подборку объявлений
        selection = Selection.objects.create(
            name="Моя подборка",
            owner=self.user
        )
        selection.items.add(self.ad)

        # Проверяем, что подборка была успешно создана
        self.assertEqual(selection.name, "Моя подборка")
        self.assertEqual(selection.owner, self.user)
        self.assertEqual(selection.items.count(), 1)
        self.assertIn(self.ad, selection.items.all())
