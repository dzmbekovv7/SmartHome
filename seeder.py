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
        "name": "Luxury Villa in Shanghai / 上海豪华别墅",
        "description": "A premium villa in Pudong with a large garden and high-end interior design.",
        "image": "houses/shanghai_luxury_villa.jpg",
        "price": 2400000,
        "location": "Shanghai, China",
        "rooms": 6,
        "square": 370,
        "has_pool": True,
        "features_internal": "Marble floors, smart lighting, wine cellar, AC",
        "features_external": "Landscaped garden, swimming pool, garage",
        "latitude": 31.2304,
        "longitude": 121.4737,
        "isVerified": True
    },
    {
        "name": "Modern Apartment in the Bund / 外滩现代公寓",
        "description": "Stylish apartment with a view of the Huangpu River and access to luxury amenities.",
        "image": "houses/shanghai_modern_apartment.jpg",
        "price": 1800000,
        "location": "Shanghai, China",
        "rooms": 3,
        "square": 190,
        "has_pool": False,
        "features_internal": "Panoramic windows, modern furniture, integrated appliances",
        "features_external": "Concierge, gym, rooftop access",
        "latitude": 31.2400,
        "longitude": 121.4900,
        "isVerified": True
    },

    # Исламабад, Пакистан
    {
        "name": "Family House in Islamabad / اسلام آباد میں خاندانی مکان",
        "description": "Spacious home ideal for families, located in a peaceful neighborhood in Islamabad.",
        "image": "houses/islamabad_family_house.jpg",
        "price": 950000,
        "location": "Islamabad, Pakistan",
        "rooms": 5,
        "square": 280,
        "has_pool": False,
        "features_internal": "Tiled flooring, AC, built-in wardrobes, prayer room",
        "features_external": "Garden, car porch, boundary wall",
        "latitude": 33.6844,
        "longitude": 73.0479,
        "isVerified": True
    },
    {
        "name": "Islamabad Hilltop Villa / اسلام آباد ہل ٹاپ ولا",
        "description": "Exclusive villa with scenic views of the Margalla Hills and luxury interiors.",
        "image": "houses/islamabad_hilltop_villa.jpg",
        "price": 1600000,
        "location": "Islamabad, Pakistan",
        "rooms": 6,
        "square": 350,
        "has_pool": True,
        "features_internal": "Wooden floors, central heating, guest suite, smart controls",
        "features_external": "Hill view, private lawn, BBQ area",
        "latitude": 33.7294,
        "longitude": 73.0931,
        "isVerified": True
    },
    {
        "name": "Smart Home in Islamabad / اسلام آباد کا سمارٹ گھر",
        "description": "A smart-enabled minimalist house perfect for professionals and small families.",
        "image": "houses/islamabad_smart_home.jpg",
        "price": 1100000,
        "location": "Islamabad, Pakistan",
        "rooms": 4,
        "square": 210,
        "has_pool": False,
        "features_internal": "Smart lighting, remote control system, modern kitchen",
        "features_external": "Small lawn, solar panels, secure entrance",
        "latitude": 33.6938,
        "longitude": 73.0652,
        "isVerified": True
    },
    {
        "name": "Коттедж в Подмосковье",
        "description": "Просторный коттедж с баней и зимним садом.",
        "image": "houses/russia_cottage_moscow.jpg",
        "price": 600000,
        "location": "Московская область, Россия",
        "rooms": 5,
        "square": 250,
        "has_pool": False,
        "features_internal": "Камин, паркет, бойлер, охранная сигнализация",
        "features_external": "Баня, сад, беседка",
        "latitude": 55.7558,
        "longitude": 37.6176,
        "isVerified": True
    },
    {
        "name": "Апартаменты в Санкт-Петербурге",
        "description": "Современные апартаменты в центре города.",
        "image": "houses/russia_apartment_spb.jpg",
        "price": 450000,
        "location": "Санкт-Петербург, Россия",
        "rooms": 3,
        "square": 120,
        "has_pool": False,
        "features_internal": "Дизайнерский ремонт, встроенная техника",
        "features_external": "Парковка, видеонаблюдение",
        "latitude": 59.9311,
        "longitude": 30.3609,
        "isVerified": True
    },
    {
        "name": "Дом на Байкале",
        "description": "Живописный дом с видом на озеро Байкал.",
        "image": "houses/russia_lake_baikal.jpg",
        "price": 380000,
        "location": "Иркутская область, Россия",
        "rooms": 4,
        "square": 180,
        "has_pool": False,
        "features_internal": "Деревянная отделка, печь, зимний сад",
        "features_external": "Терраса, вид на озеро, лодочная станция",
        "latitude": 51.8833,
        "longitude": 104.7333,
        "isVerified": True
    },

    # Япония — 5 домов
    {
        "name": "Традиционный дом в Киото",
        "description": "Красивый японский дом в стиле «матика» рядом с храмами.",
        "image": "houses/japan_kyoto_traditional.jpg",
        "price": 750000,
        "location": "Киото, Япония",
        "rooms": 3,
        "square": 130,
        "has_pool": False,
        "features_internal": "Сёдзи, татами, деревянные балки",
        "features_external": "Сад камней, бамбуковая роща",
        "latitude": 35.0116,
        "longitude": 135.7681,
        "isVerified": True
    },
    {
        "name": "Современный дом в Токио",
        "description": "Инновационный дом в мегаполисе с умными системами.",
        "image": "houses/japan_tokyo_modern.jpg",
        "price": 1200000,
        "location": "Токио, Япония",
        "rooms": 4,
        "square": 150,
        "has_pool": False,
        "features_internal": "Умный дом, солнечные панели, минимализм",
        "features_external": "Балкон, гараж",
        "latitude": 35.6895,
        "longitude": 139.6917,
        "isVerified": True
    },
    {
        "name": "Дом у горы Фудзи",
        "description": "Уютный дом с видом на гору Фудзи.",
        "image": "houses/japan_fuji_house.jpg",
        "price": 820000,
        "location": "Яманаси, Япония",
        "rooms": 3,
        "square": 140,
        "has_pool": False,
        "features_internal": "Тёплые полы, японская ванна офуро",
        "features_external": "Сад, площадка для барбекю",
        "latitude": 35.3606,
        "longitude": 138.7274,
        "isVerified": True
    },
    {
        "name": "Апартаменты в Осака",
        "description": "Современные апартаменты в бизнес-центре.",
        "image": "houses/japan_osaka_apartment.jpg",
        "price": 990000,
        "location": "Осака, Япония",
        "rooms": 2,
        "square": 100,
        "has_pool": False,
        "features_internal": "Панорамные окна, кондиционер, кухня-студия",
        "features_external": "Крыша с видом, подземная парковка",
        "latitude": 34.6937,
        "longitude": 135.5023,
        "isVerified": True
    },
    {
        "name": "Дом на острове Окинава",
        "description": "Дом у моря, идеален для отдыха.",
        "image": "houses/japan_okinawa_beachhouse.jpg",
        "price": 680000,
        "location": "Окинава, Япония",
        "rooms": 3,
        "square": 110,
        "has_pool": True,
        "features_internal": "Минималистичный интерьер, большая кухня",
        "features_external": "Бассейн, веранда, пальмы",
        "latitude": 26.3344,
        "longitude": 127.8056,
        "isVerified": True
    },

    # Южная Корея — 5 домов
    {
        "name": "Дом в Сеуле",
        "description": "Уютный семейный дом в центре столицы.",
        "image": "houses/korea_seoul_house.jpg",
        "price": 1100000,
        "location": "Сеул, Южная Корея",
        "rooms": 4,
        "square": 160,
        "has_pool": False,
        "features_internal": "Тёплый пол, умный замок, кладовая",
        "features_external": "Балкон, мини-сад",
        "latitude": 37.5665,
        "longitude": 126.9780,
        "isVerified": True
    },
    {
        "name": "Лофт в Бусане",
        "description": "Современный лофт с видом на море.",
        "image": "houses/korea_busan_loft.jpg",
        "price": 970000,
        "location": "Пусан, Южная Корея",
        "rooms": 2,
        "square": 120,
        "has_pool": False,
        "features_internal": "Высокие потолки, стеклянные стены",
        "features_external": "Близко к пляжу, парковка",
        "latitude": 35.1796,
        "longitude": 129.0756,
        "isVerified": True
    },
    {
        "name": "Коттедж в Чеджу",
        "description": "Загородный дом на острове Чеджу с видом на вулкан.",
        "image": "houses/korea_jeju_cottage.jpg",
        "price": 890000,
        "location": "Чеджу, Южная Корея",
        "rooms": 3,
        "square": 130,
        "has_pool": True,
        "features_internal": "Традиционные корейские элементы, тёплый пол",
        "features_external": "Открытая терраса, сад",
        "latitude": 33.4996,
        "longitude": 126.5312,
        "isVerified": True
    },
    {
        "name": "Пентхаус в Инчхон",
        "description": "Роскошный пентхаус с панорамным видом.",
        "image": "houses/korea_incheon_penthouse.jpg",
        "price": 1500000,
        "location": "Инчхон, Южная Корея",
        "rooms": 5,
        "square": 200,
        "has_pool": True,
        "features_internal": "Лифт в квартиру, дизайнерский интерьер",
        "features_external": "Бассейн, крыша, охрана",
        "latitude": 37.4563,
        "longitude": 126.7052,
        "isVerified": True
    },
    {
        "name": "Апартаменты в Тэгу",
        "description": "Удобные апартаменты с отличной транспортной доступностью.",
        "image": "houses/korea_daegu_apartment.jpg",
        "price": 800000,
        "location": "Тэгу, Южная Корея",
        "rooms": 3,
        "square": 110,
        "has_pool": False,
        "features_internal": "Индукционная плита, большая ванная",
        "features_external": "Парковка, сад на крыше",
        "latitude": 35.8714,
        "longitude": 128.6014,
        "isVerified": True
    },

    # США — 5 домов
    {
        "name": "Beach House in California",
        "description": "A beautiful house on the California coast with beach access.",
        "image": "houses/usa_california_beach.jpg",
        "price": 2200000,
        "location": "California, USA",
        "rooms": 4,
        "square": 200,
        "has_pool": True,
        "features_internal": "Open-plan kitchen, fireplace, smart home",
        "features_external": "Beachfront, pool, garage",
        "latitude": 34.0195,
        "longitude": -118.4912,
        "isVerified": True
    },
    {
        "name": "Apartment in New York City",
        "description": "Modern high-rise apartment with Manhattan views.",
        "image": "houses/usa_nyc_apartment.jpg",
        "price": 1800000,
        "location": "New York, USA",
        "rooms": 2,
        "square": 90,
        "has_pool": False,
        "features_internal": "Central AC, large windows, concierge service",
        "features_external": "Gym, rooftop access",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "isVerified": True
    },
    {
        "name": "Ranch in Texas",
        "description": "Spacious ranch ideal for a peaceful countryside lifestyle.",
        "image": "houses/usa_texas_ranch.jpg",
        "price": 950000,
        "location": "Texas, USA",
        "rooms": 6,
        "square": 350,
        "has_pool": True,
        "features_internal": "Rustic interior, fireplace, big kitchen",
        "features_external": "Barn, stable, open fields",
        "latitude": 31.9686,
        "longitude": -99.9018,
        "isVerified": True
    },
    {
        "name": "Suburban Home in Illinois",
        "description": "Perfect family house in a quiet Chicago suburb.",
        "image": "houses/usa_illinois_suburb.jpg",
        "price": 700000,
        "location": "Illinois, USA",
        "rooms": 4,
        "square": 180,
        "has_pool": False,
        "features_internal": "Hardwood floors, basement, 2-car garage",
        "features_external": "Backyard, playground",
        "latitude": 41.8781,
        "longitude": -87.6298,
        "isVerified": True
    },
    {
        "name": "Modern House in Miami",
        "description": "Luxury house with pool and palm trees.",
        "image": "houses/usa_miami_modern.jpg",
        "price": 1400000,
        "location": "Miami, USA",
        "rooms": 3,
        "square": 160,
        "has_pool": True,
        "features_internal": "Smart home, marble floors",
        "features_external": "Palm garden, pool, outdoor kitchen",
        "latitude": 25.7617,
        "longitude": -80.1918,
        "isVerified": True
    },

    # Кыргызстан — 5 домов
    {
        "name": "Дом в Бишкеке",
        "description": "Уютный семейный дом в столице Кыргызстана.",
        "image": "houses/kyrgyzstan_bishkek.jpg",
        "price": 300000,
        "location": "Бишкек, Кыргызстан",
        "rooms": 4,
        "square": 160,
        "has_pool": False,
        "features_internal": "Газовое отопление, плитка, кладовая",
        "features_external": "Сад, парковка",
        "latitude": 42.8746,
        "longitude": 74.5698,
        "isVerified": True
    },
    {
        "name": "Горный дом в Чон-Кемине",
        "description": "Дом в живописной долине Чон-Кемин.",
        "image": "houses/kyrgyzstan_chonkemin.jpg",
        "price": 250000,
        "location": "Чон-Кемин, Кыргызстан",
        "rooms": 3,
        "square": 140,
        "has_pool": False,
        "features_internal": "Печь, деревянная отделка",
        "features_external": "Сарай, фруктовый сад",
        "latitude": 42.8333,
        "longitude": 75.0833,
        "isVerified": True
    },
    {
        "name": "Коттедж у озера Иссык-Куль",
        "description": "Дом для отдыха у берега озера.",
        "image": "houses/kyrgyzstan_issyk_kul.jpg",
        "price": 400000,
        "location": "Иссык-Куль, Кыргызстан",
        "rooms": 4,
        "square": 170,
        "has_pool": True,
        "features_internal": "Современный интерьер, сауна",
        "features_external": "Бассейн, терраса, пляж рядом",
        "latitude": 42.4500,
        "longitude": 77.1833,
        "isVerified": True
    },
    {
        "name": "Дом в Оше",
        "description": "Недорогой дом в центре города.",
        "image": "houses/kyrgyzstan_osh.jpg",
        "price": 200000,
        "location": "Ош, Кыргызстан",
        "rooms": 3,
        "square": 130,
        "has_pool": False,
        "features_internal": "Плитка, ванная комната, кухня",
        "features_external": "Маленький двор, забор",
        "latitude": 40.5283,
        "longitude": 72.7985,
        "isVerified": True
    },
    {
        "name": "Сельский дом в Нарыне",
        "description": "Простой дом для спокойной жизни в горах.",
        "image": "houses/kyrgyzstan_naryn.jpg",
        "price": 180000,
        "location": "Нарын, Кыргызстан",
        "rooms": 2,
        "square": 100,
        "has_pool": False,
        "features_internal": "Печь, скромная отделка",
        "features_external": "Хлев, участок земли",
        "latitude": 41.4287,
        "longitude": 75.9911,
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



