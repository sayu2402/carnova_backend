from django.urls import path
from .views import *


urlpatterns=[
    path('vendor-profile/<int:user_id>/', VendorProfileView.as_view(), name='vendor-profile'),
    path('vendor-edit/<int:user_id>/', VendorProfileUpdateView.as_view(), name='user-edit'),
    path('change-password/<int:user_id>/', VendorChangePasswordView.as_view(), name='change-password'),
    path('add-car/<int:vendor_id>/', AddCarView.as_view(), name='add-car'),
    path('car-details/<int:vendor_id>/', VendorCarDetailsView.as_view(), name='vendor-car-details'),
    path('edit-car/<int:car_id>/', EditCarDetailsView.as_view(), name='edit-car-details'),
    path('bookings/<int:id>/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/update-status/', UpdateBookingStatusView.as_view(), name='update-booking-status'),
    path('chart/<int:user_id>/', VendorStatsAPIView.as_view(), name='chart_data'),
    path('pie-chart/<int:vendor_id>/', PieChartVendorDataView.as_view(), name='vendor-pie-chart-data'),
]