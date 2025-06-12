import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# Define rent per square meter (these are example values, adjust as needed)
rent_per_m2 = {
    'Bishkek': 7000,
    'Osh': 5000,
    'Chuy Region': 6000,
    'Issyk-Kul Region': 2500,
    'Batken Region': 1500,
    'Talas Region': 2000,
    'Jalal-Abad Region': 2200
}

# Multipliers might be different for rent, e.g. less steep than for purchase price
property_type_rent_multipliers = {
    'Apartment': 1.0,
    'House': 1.1,
    'Cottage': 1.2,
    'Villa': 1.4
}

rent_data = []

for region, rent_m2 in rent_per_m2.items():
    for property_type, type_multiplier in property_type_rent_multipliers.items():
        for area in range(30, 301, 10):
            bedrooms = max(1, area // 40)
            bathrooms = max(1, area // 70)
            floors = 1 if area <= 100 else 2 if area <= 200 else 3
            has_pool = 1 if area >= 120 else 0

            base_rent = area * rent_m2 * type_multiplier

            bedroom_multiplier = 1 + (bedrooms - 1) * 0.02  # less effect for rent
            bathroom_multiplier = 1 + (bathrooms - 1) * 0.015
            floor_multiplier = 1 + (floors - 1) * 0.03
            pool_multiplier = 1.1 if has_pool else 1.0

            total_multiplier = bedroom_multiplier * bathroom_multiplier * floor_multiplier * pool_multiplier
            rent = base_rent * total_multiplier

            rent_data.append({
                'area': area,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'floors': floors,
                'has_pool': has_pool,
                'property_type': property_type,
                'region': region,
                'rent': round(rent)
            })

df_rent = pd.DataFrame(rent_data)
X_rent = df_rent.drop('rent', axis=1)
y_rent = df_rent['rent']

categorical_features = ['property_type', 'region']
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(
    transformers=[('cat', categorical_transformer, categorical_features)],
    remainder='passthrough'
)

rent_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

rent_model.fit(X_rent, y_rent)

# Save the rent model separately
os.makedirs("realestate/ml_model/models", exist_ok=True)
joblib.dump(rent_model, "realestate/ml_model/models/rent_model.pkl")
print("✅ Rent prediction model trained and saved.")
