from django.urls import path
from .views import *


urlpatterns=[
    path('cars-list/',CarsList.as_view(), name='user-edit'),
    path('verify-car/<int:pk>/',VerifyCarView.as_view(), name='user-edit'),
    path('car-details/<int:id>/', CarDetailsView.as_view(), name='car-details-api'),
]