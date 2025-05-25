from rest_framework import serializers
from .models import PredictionHistory

class PredictionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionHistory
        fields = [
            'id',
            'prediction_type',
            'sqft',
            'bedrooms',
            'bathrooms',
            'floors',
            'has_pool',
            'property_type',
            'region',
            'predicted_value',
            'created_at',
        ]
