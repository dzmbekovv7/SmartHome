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
        title = "House Prices"
        ylabel = "Price (USD)"
        filename = "price_chart.png"
    elif chart_type == "sales":
        data = df["sales"]
        title = "House Sales"
        ylabel = "Sales"
        filename = "sales_chart.png"
    elif chart_type == "size":
        data = df["size"]
        title = "House Size"
        ylabel = "m²"
        filename = "size_chart.png"
    elif chart_type == "district":
        # Example placeholder, logic by district needs to be added
        data = df["price"]  # for example, prices by districts — replace according to your dataset
        title = "Chart by Districts (example)"
        ylabel = "Price (USD)"
        filename = "district_chart.png"
    else:
        return None

    plt.figure(figsize=(6, 4))
    plt.plot(years, data, marker='o')
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.grid(True)

    file_path = os.path.join(charts_dir, filename)
    plt.savefig(file_path)
    plt.close()

    return settings.MEDIA_URL + f"charts/{filename}"
