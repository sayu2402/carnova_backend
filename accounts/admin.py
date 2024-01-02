from django.contrib import admin
from .models import *

#Register your models here.

admin.site.register(UserAccount)
admin.site.register(UserProfile)
admin.site.register(VendorProfile)
admin.site.register(AdminProfile)