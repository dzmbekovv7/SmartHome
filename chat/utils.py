import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "data", "housing_kg.csv")
df = pd.read_csv(csv_path)

charts_dir = os.path.join(settings.MEDIA_ROOT, "charts")
os.makedirs(charts_dir, exist_ok=True)

def generate_chart(chart_type="price") -> str | None:
    years = df["year"]

    if chart_type == "price":
        data = df["price"]
        title = "Цены на дома"
        ylabel = "Цена (USD)"
        filename = "price_chart.png"
    elif chart_type == "sales":
        data = df["sales"]
        title = "Продажи домов"
        ylabel = "Продажи"
        filename = "sales_chart.png"
    elif chart_type == "size":
        data = df["size"]
        title = "Площадь домов"
        ylabel = "м²"
        filename = "size_chart.png"
    elif chart_type == "district":
        # Пример заглушки, надо добавить логику по районам
        data = df["price"]  # например, цены по районам — замените по своему датасету
        title = "График по районам (пример)"
        ylabel = "Цена (USD)"
        filename = "district_chart.png"
    else:
        return None

    plt.figure(figsize=(6, 4))
    plt.plot(years, data, marker='o')
    plt.title(title)
    plt.xlabel("Год")
    plt.ylabel(ylabel)
    plt.grid(True)

    file_path = os.path.join(charts_dir, filename)
    plt.savefig(file_path)
    plt.close()

    return settings.MEDIA_URL + f"charts/{filename}"
