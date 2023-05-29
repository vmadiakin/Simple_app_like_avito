import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DZ27.settings")
django.setup()

from ads.models import Category, Ad

# Загрузка данных из categories.json
with open('./datasets/categories.json', 'r', encoding='utf-8') as categories_file:
    categories_data = json.load(categories_file)

# Загрузка данных из ads.json
with open('./datasets/ads.json', 'r', encoding='utf-8') as ads_file:
    ads_data = json.load(ads_file)

# Создание категорий
for category_data in categories_data:
    category_id = category_data['id']
    category_name = category_data['name']
    Category.objects.create(id=category_id, name=category_name)

# Создание объявлений
for ad_data in ads_data:
    ad_id = ad_data['Id']
    ad_name = ad_data['name']
    ad_author = ad_data['author']
    ad_price = ad_data['price']
    ad_description = ad_data['description']
    ad_address = ad_data['address']
    ad_is_published = ad_data['is_published'].title()  # Преобразование значения в булево

    Ad.objects.create(
        id=ad_id,
        name=ad_name,
        author=ad_author,
        price=ad_price,
        description=ad_description,
        address=ad_address,
        is_published=ad_is_published
    )

print("Data imported successfully.")
