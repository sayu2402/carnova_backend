from django.db import models
from accounts.models import VendorProfile

class CarHandling(models.Model):
    FUEL_CHOICES = [
        ('Diesel', 'Diesel'),
        ('Petrol', 'Petrol'),
        ('Electric', 'Electric'),
    ]

    TRANSMISSION_CHOICES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
    ]

    CATEGORY_CHOICES = [
        ('Premium', 'Premium'),
        ('Medium', 'Medium'),
        ('Normal', 'Normal'),
    ]

    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    location = models.CharField(max_length=100)
    model = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    car_photo = models.ImageField(upload_to='')
    document = models.FileField(upload_to='')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.car_name}"
