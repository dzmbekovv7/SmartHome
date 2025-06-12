import joblib
import os
import pandas as pd

# Загрузка модели
model_path = os.path.join(os.path.dirname(__file__), 'models', 'price_model.pkl')
model = joblib.load(model_path)

def predict_price(area, bedrooms, bathrooms, floors, has_pool, property_type, region):
    has_pool = int(has_pool)

    # Формируем DataFrame с нужными колонками
    input_data = pd.DataFrame([{
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'floors': floors,
        'has_pool': has_pool,
        'property_type': property_type,
        'region': region
    }])

    # Предсказание
    predicted_price = model.predict(input_data)[0]
    return round(predicted_price)
