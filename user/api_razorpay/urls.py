# car/urls.py
from django.urls import path
from .api_razorpay import CreateCarBookingAPIView, CreateCarOrderAPIView

urlpatterns = [
    path('car/order/<int:carId>/<str:pickupDate>/<str:returnDate>/<int:userId>/', 
         CreateCarOrderAPIView.as_view(), 
         name='create-car-order'),

    path(
        'car/book/<int:carId>/<str:pickupDate>/<str:returnDate>/<int:userId>/',
        CreateCarBookingAPIView.as_view(),
        name='create-car-booking'
    ),
]
