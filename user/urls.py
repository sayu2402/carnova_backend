from django.urls import path
from .views import *


urlpatterns=[
    path('user-edit/<int:user_id>/',ProfileUpdateView.as_view(), name='user-edit'),
    path('userprofile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
]