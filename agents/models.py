from django.db import models
from django.conf import settings

class Agency(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class AgencyCompany(models.Model):
    name = models.CharField(max_length=255)
    logo = models.URLField()
    description = models.TextField()
    website = models.URLField()

    def __str__(self):
        return self.name

class Advantage(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Review(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"Отзыв от {self.name}"

class AgentApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=50)
    passport_issued_by = models.CharField(max_length=255, null=True, blank=True)
    passport_issue_date = models.DateField( null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)  # ← добавьте это поле
    address = models.CharField(max_length=500, null=True, blank=True)  # изменено
    additional_info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.user.username}"
