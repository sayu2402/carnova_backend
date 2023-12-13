from django.urls import path
from .views import *


urlpatterns=[
    path('user-edit/<int:user_id>/',ProfileUpdateView.as_view(), name='user-edit'),
    path('userprofile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/<int:user_id>/', ChangePasswordView.as_view(), name='change-password'),
    path('browse-cars/', CarBrowseView.as_view(), name='car-browse'),
    path('car-details/<int:car_id>/', CarDetailView.as_view(), name='car-details'),
]