import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

price_per_m2 = {
    'Bishkek': 129_290,
    'Osh': 95_138,
    'Chuy Region': 107_953,
    'Issyk-Kul Region': 38_063,
    'Batken Region': 18_237,
    'Talas Region': 44_302,
    'Jalal-Abad Region': 46_798
}

property_type_multipliers = {
    'Apartment': 1.0,
    'House': 1.15,
    'Cottage': 1.3,
    'Villa': 1.5
}

data = []

for region, price_m2 in price_per_m2.items():
    for property_type, type_multiplier in property_type_multipliers.items():
        for area in range(30, 301, 10):  # from 30 to 300 m²
            bedrooms = max(1, area // 40)
            bathrooms = max(1, area // 70)
            floors = 1 if area <= 100 else 2 if area <= 200 else 3
            has_pool = 1 if area >= 120 else 0

            base_price = area * price_m2 * type_multiplier

            bedroom_multiplier = 1 + (bedrooms - 1) * 0.03
            bathroom_multiplier = 1 + (bathrooms - 1) * 0.025
            floor_multiplier = 1 + (floors - 1) * 0.05
            pool_multiplier = 1.15 if has_pool else 1.0

            total_multiplier = bedroom_multiplier * bathroom_multiplier * floor_multiplier * pool_multiplier
            price = base_price * total_multiplier

            data.append({
                'area': area,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'floors': floors,
                'has_pool': has_pool,
                'property_type': property_type,
                'region': region,
                'price': round(price)
            })

df = pd.DataFrame(data)
X = df.drop('price', axis=1)
y = df['price']

categorical_features = ['property_type', 'region']
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(
    transformers=[('cat', categorical_transformer, categorical_features)],
    remainder='passthrough'
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

model.fit(X, y)

# Save the model
os.makedirs("realestate/ml_model/models", exist_ok=True)
joblib.dump(model, "realestate/ml_model/models/price_model.pkl")
print("✅ Model trained with property type taken into account and saved.")
