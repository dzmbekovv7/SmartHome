# models.py

from django.db import models
from django.conf import settings
class Sale(models.Model):
    date = models.DateField()
    price = models.FloatField()
    region = models.CharField(max_length=100)
class PredictionHistory(models.Model):
    PREDICTION_TYPE_CHOICES = (
        ('price', 'Price'),
        ('rent', 'Rent'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prediction_type = models.CharField(max_length=10, choices=PREDICTION_TYPE_CHOICES)
    sqft = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    floors = models.IntegerField()
    has_pool = models.BooleanField(default=False)
    property_type = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    predicted_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction_type} - {self.predicted_value}"
