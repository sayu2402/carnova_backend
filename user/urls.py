from django.urls import path
from .views import *


urlpatterns=[
    path('user-edit/<int:user_id>/',ProfileUpdateView.as_view(), name='user-edit'),
    path('userprofile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/<int:user_id>/', ChangePasswordView.as_view(), name='change-password'),
    path('browse-cars/', CarBrowseView.as_view(), name='car-browse'),
    path('car-details/<int:car_id>/', CarDetailView.as_view(), name='car-details'),
    path('car-availability/<int:carId>/<str:pickupDate>/<str:returnDate>/', 
         CarAvailabilityAPIView.as_view(), 
         name='check-car-availability'),
    path('google-login/', UserGoogleLogin.as_view(), name='google-login'),
    path('bookings/<int:user_id>/', BookingList.as_view(), name='booking-list'),
    path('booking-detail/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('wallet/<int:user_id>/', WalletMoney.as_view(), name='wallet'),
    path('cancel-booking/<int:user_id>/<int:booking_id>/', CancelOrder.as_view(), name='cancel-order')
]