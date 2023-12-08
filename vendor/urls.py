from django.urls import path
from .views import *


urlpatterns=[
    path('vendor-profile/<int:user_id>/', VendorProfileView.as_view(), name='vendor-profile'),
    path('vendor-edit/<int:user_id>/', VendorProfileUpdateView.as_view(), name='user-edit'),

]