from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAccount(AbstractUser):
    ROLES = (
        ('user', 'User'),
        ('partner', 'Partner'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username','role','phone_no']

    role = models.CharField(max_length=10, choices=ROLES, default='user')
    phone_no = models.CharField(max_length=30, unique=True, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='image_profiles/', blank=True, null=True)


    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='user_profile')

    def __str__(self):
        return str(self.user)

class VendorProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='vendor_profile')
    
    def __str__(self):
        return str(self.user)

class AdminProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return str(self.user)
