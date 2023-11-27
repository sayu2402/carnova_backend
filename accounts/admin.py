from django.contrib import admin
from .models import UserAccount,UserProfile,VendorProfile

#Register your models here.

admin.site.register(UserAccount)
admin.site.register(UserProfile)
admin.site.register(VendorProfile)
