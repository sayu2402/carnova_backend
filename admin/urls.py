from django.urls import path
from .views import *


urlpatterns=[
    path('cars-list/',CarsList.as_view(), name='user-edit'),
    path('verify-car/<int:pk>/',VerifyCarView.as_view(), name='user-edit'),
    path('car-details/<int:id>/', CarDetailsView.as_view(), name='car-details-api'),
    path('bookings-list/', BookingListView.as_view(), name='admin-booking-list'),
    path('api/send-morning-emails/', index, name='send_morning_emails'),

]