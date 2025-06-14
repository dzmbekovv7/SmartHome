from django.db import models
from django.conf import settings
import uuid

class EmailVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)  # Было: models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - Verified: {self.is_verified}"
class House(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField(max_length=500, blank=True, null=True)
    price = models.FloatField()
    location = models.CharField(max_length=100)
    # Уберём location как просто строку и добавим координаты
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    rooms = models.IntegerField()
    square = models.IntegerField()
    has_pool = models.BooleanField()

    # Новые поля
    features_internal = models.TextField(blank=True, null=True)
    features_external = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    isVerified = models.BooleanField(default=False)

    # Track who posted the house
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='houses')
    seller_number = models.CharField(max_length=20)

    # Likes (users who liked)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_houses', blank=True)

    def like_count(self):
        return self.liked_by.count()

    def view_count(self):
        return self.views.count()

    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return self.name

class View(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Например, 'USD'
    rate = models.DecimalField(max_digits=10, decimal_places=4)  # Курс к базовой валюте
    description = models.CharField(max_length=255, blank=True)  # Название валюты
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code}: {self.rate}"