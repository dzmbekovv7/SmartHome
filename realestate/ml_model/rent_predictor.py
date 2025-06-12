import joblib
import os
import pandas as pd

# Load rent model (adjust path as needed)
rent_model_path = os.path.join(os.path.dirname(__file__), 'models', 'rent_model.pkl')
rent_model = joblib.load(rent_model_path)

def predict_rent(area, bedrooms, bathrooms, floors, has_pool, property_type, region):
    has_pool = int(has_pool)
    input_data = pd.DataFrame([{
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'floors': floors,
        'has_pool': has_pool,
        'property_type': property_type,
        'region': region
    }])
    predicted_rent = rent_model.predict(input_data)[0]
    return round(predicted_rent)
