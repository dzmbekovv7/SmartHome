import joblib
import os
import pandas as pd

# Загрузка модели аренды
model_path = os.path.join(os.path.dirname(__file__), 'models', 'rent_model.pkl')
rent_model = joblib.load(model_path)

def predict_rent(area, bedrooms, bathrooms, floors, has_pool, property_type, region):
    # Преобразуем в int (1 или 0), если передали как True/False
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
    predicted_rent = rent_model.predict(input_data)[0]
    return round(predicted_rent)
