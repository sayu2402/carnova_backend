from django.urls import path
from .views import *


urlpatterns = [
    path("cars-list/", CarsList.as_view(), name="user-edit"),
    path("verify-car/<int:pk>/", VerifyCarView.as_view(), name="user-edit"),
    path("car-details/<int:id>/", CarDetailsView.as_view(), name="car-details-api"),
    path("bookings-list/", BookingListView.as_view(), name="admin-booking-list"),
    path("chart/", ChartDataView.as_view(), name="chart_data"),
    path("pie-chart-data/", PieChartAdminDataView.as_view(), name="pie-chart-data"),
    path("new-users/", Last5UsersAPIView.as_view(), name="new-user"),
    path("new-vendors/", Last5VendorsAPIView.as_view(), name="new-vendor"),
    path("new-bookings/", Last5Booking.as_view(), name="new-booking"),
    path("block-user/<int:user_id>/", BlockUserView.as_view(), name="block_user"),
    path(
        "block-vendor/<int:vendor_id>/", BlockVendorView.as_view(), name="block_vendor"
    ),
]
