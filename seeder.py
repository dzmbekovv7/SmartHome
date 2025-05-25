import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartHomeProject.settings")
django.setup()

from houses.models import House
from django.contrib.auth import get_user_model

User = get_user_model()

# Пример данных для заполнения
houses_data = [
    {
        "name": "Современный дом у моря",
        "description": "Просторный дом с панорамными окнами, видом на океан и большой террасой.",
        "image": "houses/modern_sea_house.jpg",
        "price": 1200000,
        "location": "Геленджик, Россия",
        "rooms": 5,
        "square": 350,
        "has_pool": True,
        "features_internal": "Кондиционер, теплые полы, система умный дом, камин",
        "features_external": "Бассейн, сад, терраса, барбекю зона",
        "latitude": 44.5633,
        "longitude": 38.0761,
        "isVerified": True
    },
    {
        "name": "Уютный дом в горах",
        "description": "Каменный дом с деревянными элементами, идеален для отдыха зимой и летом.",
        "image": "houses/mountain_cozy_cottage.jpg",
        "price": 850000,
        "location": "Красная Поляна, Россия",
        "rooms": 4,
        "square": 220,
        "has_pool": False,
        "features_internal": "Деревянные балки, камин, сауна, теплый пол",
        "features_external": "Большой участок, гараж, зона отдыха на улице",
        "latitude": 43.6763,
        "longitude": 40.2923,
        "isVerified": True
    },
    {
        "name": "Современный пентхаус в центре",
        "description": "Апартаменты с видом на город, дизайнерский ремонт и все удобства.",
        "image": "houses/city_penthouse.jpg",
        "price": 1750000,
        "location": "Москва, Россия",
        "rooms": 3,
        "square": 150,
        "has_pool": False,
        "features_internal": "Дизайнерский ремонт, система 'умный дом', встроенная техника",
        "features_external": "Консьерж, подземный паркинг, фитнес-зал",
        "latitude": 55.7558,
        "longitude": 37.6173,
        "isVerified": True
    },
    {
        "name": "Дом с виноградником",
        "description": "Загородный дом с собственным виноградником и большим участком земли.",
        "image": "houses/vineyard_house.jpg",
        "price": 950000,
        "location": "Краснодарский край, Россия",
        "rooms": 6,
        "square": 400,
        "has_pool": True,
        "features_internal": "Большая кухня, камин, гостиная с панорамным окном",
        "features_external": "Виноградник, бассейн, гараж, сад",
        "latitude": 45.0345,
        "longitude": 39.0325,
        "isVerified": False
    },
    {
        "name": "Минималистичный дом у озера",
        "description": "Дом с минималистичным дизайном, панорамными окнами и выходом на озеро.",
        "image": "houses/lake_minimal_house.jpg",
        "price": 700000,
        "location": "Ладожское озеро, Россия",
        "rooms": 3,
        "square": 130,
        "has_pool": False,
        "features_internal": "Открытая планировка, панорамные окна, камин",
        "features_external": "Причал, сад, зона барбекю",
        "latitude": 60.9125,
        "longitude": 30.3370,
        "isVerified": True
    }
]

def run():
    print("Начинаем заполнение базы домов...")

    users = list(User.objects.all())
    if not users:
        print("Нет доступных пользователей для назначения продавца. Создай хотя бы одного пользователя.")
        return

    for house_data in houses_data:
        seller = random.choice(users)
        house = House.objects.create(
            name=house_data["name"],
            description=house_data["description"],
            image=house_data["image"],
            price=house_data["price"],
            location=house_data["location"],
            rooms=house_data["rooms"],
            square=house_data["square"],
            has_pool=house_data["has_pool"],
            isVerified=house_data["isVerified"],
            seller=seller,
            features_internal=house_data.get("features_internal", ""),
            features_external=house_data.get("features_external", ""),
            latitude=house_data.get("latitude", 0.0),
            longitude=house_data.get("longitude", 0.0),
        )
        print(f"Добавлен дом: {house.name} (продавец: {seller.username})")

    print("Заполнение завершено.")

if __name__ == "__main__":
    run()
