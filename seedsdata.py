import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartHomeProject.settings')
django.setup()

import datetime
from realestate.models import Sale

def run():
    # Очистим данные для чистоты
    Sale.objects.all().delete()

    regions = [
        'Бишкек',
        'Ош',
        'Чуй',
        'Жалал-Абад',
        'Нарын',
        'Ысык-Куль',
        'Талас',
        'Баткен',
        'Иссык-Куль'
    ]

    base_date = datetime.date.today()
    sales = []
    for day_offset in range(30):
        date = base_date - datetime.timedelta(days=day_offset)
        for region in regions:
            price = 10000 + day_offset * 50 + hash(region) % 5000
            sale = Sale(date=date, price=price, region=region)
            sales.append(sale)

    Sale.objects.bulk_create(sales)
    print(f"Seeded {len(sales)} sales for Кыргызстан.")

if __name__ == '__main__':
    run()
