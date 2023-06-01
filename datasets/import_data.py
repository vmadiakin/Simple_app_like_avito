import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DZ27.settings")
django.setup()

from ads.models import Ad
from categories.models import Category
from users.models import Location, User

# Загрузка данных из categories.json
with open('./datasets/categories.json', 'r', encoding='utf-8') as categories_file:
    categories_data = json.load(categories_file)

# Загрузка данных из ads.json
with open('./datasets/ads.json', 'r', encoding='utf-8') as ads_file:
    ads_data = json.load(ads_file)

# Загрузка данных из users.json
with open('./datasets/user.json', 'r', encoding='utf-8') as user_file:
    users_data = json.load(user_file)

# Загрузка данных из location.json
with open('./datasets/location.json', 'r', encoding='utf-8') as location_file:
    location_data = json.load(location_file)

# Создание местоположений
for location_data in location_data:
    location_name = location_data['name']
    location_lat = location_data['lat']
    location_lng = location_data['lng']

    Location.objects.create(
        name=location_name,
        lat=location_lat,
        lng=location_lng
    )

# Создание пользователей
for user_data in users_data:
    user_first_name = user_data['first_name']
    user_last_name = user_data['last_name']
    user_username = user_data['username']
    user_password = user_data['password']
    user_role = user_data['role']
    user_age = user_data['age']
    user_location_id = user_data['location_id']

    User.objects.create(
        first_name=user_first_name,
        last_name=user_last_name,
        username=user_username,
        password=user_password,
        role=user_role,
        age=user_age,
        location_id=user_location_id
    )

# Создание категорий
for category_data in categories_data:
    category_name = category_data['name']
    Category.objects.create(name=category_name)

# Создание объявлений
for ad_data in ads_data:
    ad_name = ad_data['name']
    ad_author_id = User.objects.get(id=ad_data['author_id'])
    ad_price = ad_data['price']
    ad_description = ad_data['description']
    ad_is_published = ad_data['is_published'].title()
    ad_category_id = ad_data['category_id']

    ad = Ad.objects.create(
        name=ad_name,
        author=ad_author_id,
        price=ad_price,
        description=ad_description,
        is_published=ad_is_published,
        category_id=ad_category_id
    )

print("Data imported successfully.")
