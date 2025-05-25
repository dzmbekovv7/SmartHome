import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartHomeProject.settings")
django.setup()

from agents.models import AgencyCompany, Advantage, Review

def run():
    # Очистим таблицы (если нужно)
    AgencyCompany.objects.all().delete()
    Advantage.objects.all().delete()
    Review.objects.all().delete()

    # Добавим агентства
    agencies = [
        {
            "name": "Kyrgyz Недвижимость",
            "logo": "https://cdn.house.kg/house/dealers/221ec35054b78f21b1bd5bcf0fb34587_logo.jpg",
            "description": "Ведущее агентство недвижимости в Кыргызстане.",
            "website": "https://kyrgyzrealestate.kg",
        },
        {
            "name": "КУТ",
            "logo": "https://kutned.kg/logo.svg",
            "description": "Лучшие предложения по недвижимости в Бишкеке.",
            "website": "https://bishkekhomes.kg",
        },
        {
            "name": "Amanat",
            "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQObgQoiKjCpqNtXCIa4MqbGgQ9orK33Vyp97Vj9lAeFgcKbjJf0x_VV0jyykwy6vgGM8&usqp=CAU",
            "description": "Надежное агентство с широким выбором квартир.",
            "website": "https://asiarealty.kg",
        },
    ]

    for agency in agencies:
        AgencyCompany.objects.create(**agency)

    # Добавим преимущества
    advantages = [
        {"text": "Большой выбор недвижимости по выгодным ценам"},
        {"text": "Профессиональная команда консультантов"},
        {"text": "Индивидуальный подход к каждому клиенту"},
        {"text": "Гарантия юридической чистоты сделки"},
    ]

    for adv in advantages:
        Advantage.objects.create(**adv)

    # Добавим отзывы
    reviews = [
        {"name": "Айжан", "text": "Очень довольна работой агентства, всё прошло гладко."},
        {"name": "Эркин", "text": "Спасибо за помощь в подборе квартиры. Рекомендую!"},
        {"name": "Динара", "text": "Отличный сервис и профессиональный подход."},
    ]

    for review in reviews:
        Review.objects.create(**review)

    print("Данные успешно добавлены в базу!")

if __name__ == "__main__":
    run()
