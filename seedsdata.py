import os
import django
from datetime import timedelta, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartHomeProject.settings')
django.setup()
import random

import datetime
from realestate.models import Sale

# Удаляем старые данные
Sale.objects.all().delete()

regions = ['Бишкек', 'Ош', 'Токмок', 'Каракол', 'Нарын', 'Талас']
base_date = date.today() - timedelta(days=60)

print("Создание данных продаж...")

for i in range(60):
    current_date = base_date + timedelta(days=i)
    for _ in range(random.randint(3, 8)):  # продажи в день
        Sale.objects.create(
            date=current_date,
            price=random.uniform(20000, 150000),
            region=random.choice(regions)
        )

print("✅ Данные успешно добавлены.")