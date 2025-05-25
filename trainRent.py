import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# Цена аренды за м² (условные, можно заменить на реальные при наличии)
rent_per_m2 = {
    'Бишкек': 750,
    'Ош': 600,
    'Чуйская область': 650,
    'Иссык-Кульская область': 400,
    'Баткенская область': 300,
    'Таласская область': 350,
    'Джалал-Абадская область': 370
}

property_type_multipliers = {
    'Квартира': 1.0,
    'Дом': 1.1,
    'Коттедж': 1.25,
    'Вилла': 1.4
}

data = []

for region, rent_m2 in rent_per_m2.items():
    for property_type, type_multiplier in property_type_multipliers.items():
        for area in range(30, 301, 10):
            bedrooms = max(1, area // 40)
            bathrooms = max(1, area // 70)
            floors = 1 if area <= 100 else 2 if area <= 200 else 3
            has_pool = 1 if area >= 120 else 0

            base_rent = area * rent_m2 * type_multiplier

            bedroom_multiplier = 1 + (bedrooms - 1) * 0.025
            bathroom_multiplier = 1 + (bathrooms - 1) * 0.02
            floor_multiplier = 1 + (floors - 1) * 0.03
            pool_multiplier = 1.1 if has_pool else 1.0

            total_multiplier = bedroom_multiplier * bathroom_multiplier * floor_multiplier * pool_multiplier
            rent_price = base_rent * total_multiplier

            data.append({
                'area': area,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'floors': floors,
                'has_pool': has_pool,
                'property_type': property_type,
                'region': region,
                'price': round(rent_price)
            })

df = pd.DataFrame(data)

# Фичи и целевая переменная
X = df.drop('price', axis=1)
y = df['price']

# Препроцессинг для категориальных признаков
categorical_features = ['property_type', 'region']
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(
    transformers=[('cat', categorical_transformer, categorical_features)],
    remainder='passthrough'
)

# Создаем pipeline с линейной регрессией
rent_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Обучение модели
rent_model.fit(X, y)

# Сохраняем модель
os.makedirs("realestate/ml_model/models", exist_ok=True)
joblib.dump(rent_model, "realestate/ml_model/models/rent_model.pkl")
print("✅ Модель аренды обучена и сохранена как rent_model.pkl")

# 📊 Построение графика распределения цен
plt.figure(figsize=(10, 6))
plt.hist(df['price'], bins=40, color='skyblue', edgecolor='black')
plt.title("Распределение цен аренды")
plt.xlabel("Цена аренды")
plt.ylabel("Количество объектов")
plt.grid(True)
plt.tight_layout()
plt.savefig("realestate/ml_model/rent_price_distribution.png")
plt.show()
