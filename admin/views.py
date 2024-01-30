from rest_framework.generics import ListAPIView
from django.views import View
from rest_framework.views import APIView
from vendor.models import CarHandling
from rest_framework.response import Response
from rest_framework import status, generics
from .serializer import CarHandlingSerializer
from rest_framework.generics import RetrieveAPIView
from user.models import Booking, Transcation
from user.serializer import BookingSerializer
from rest_framework.pagination import PageNumberPagination
from admin.tasks import *
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models import Count
from accounts.serializer import *
from django.shortcuts import get_object_or_404


# Create your views here.


class CarsList(ListAPIView):
    serializer_class = CarHandlingSerializer
    queryset = CarHandling.objects.all().order_by("-id")
    pagination_class = PageNumberPagination
    page_size = 6  # Set your desired page size
    page_size_query_param = "page_size"
    max_page_size = 100

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Serialize the data, including the vendor name
        serialized_cars = []
        for car in queryset:
            car_data = self.get_serializer(car).data
            car_data["vendor_name"] = car.vendor.user.username
            serialized_cars.append(car_data)

        # Return paginated response
        page = self.paginate_queryset(serialized_cars)
        return self.get_paginated_response(page) if page else Response(serialized_cars)


class VerifyCarView(generics.UpdateAPIView):
    queryset = CarHandling.objects.all()
    serializer_class = CarHandlingSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        verification_status = request.data.get("verification_status", None)

        if verification_status not in ["Approved", "Rejected"]:
            return Response(
                {"error": "Invalid verification status"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.verification_status = verification_status
        instance.save()

        # Include vendor_name in the response data
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data["vendor_name"] = instance.vendor.user.username

        return Response(response_data, status=status.HTTP_200_OK)


class CarDetailsView(RetrieveAPIView):
    queryset = CarHandling.objects.all()
    serializer_class = CarHandlingSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data

        # Include vendor_name in the response data
        response_data["vendor_name"] = instance.vendor.user.username

        return Response(response_data, status=status.HTTP_200_OK)


class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all().order_by("-id")
    serializer_class = BookingSerializer


class ChartDataView(View):
    def get(self, request, *args, **kwargs):
        # Calculate total revenue
        total_revenue = (
            Transcation.objects.aggregate(Sum("company_share"))["company_share__sum"]
            or 0
        )

        # Count number of bookings
        bookings_count = Booking.objects.count()

        # Count total cars
        total_cars = CarHandling.objects.count()

        total_vendor = VendorProfile.objects.count()

        monthly_revenue = (
            Transcation.objects.filter(transaction_date__month=1).aggregate(
                Sum("company_share")
            )["company_share__sum"]
            or 0
        )

        data = {
            "totalRevenue": total_revenue,
            "bookings": bookings_count,
            "totalCars": total_cars,
            "monthlyRevenue": monthly_revenue,
            "total_vendor": total_vendor,
        }

        return JsonResponse(data)


class PieChartAdminDataView(View):
    def get(self, request, *args, **kwargs):
        verification_choices = dict(CarHandling.VERIFICATION_CHOICES)
        verification_data = CarHandling.objects.values("verification_status").annotate(
            count=Count("verification_status")
        )

        # Initialize counts for all choices, even if they are not present in the database
        data = {
            "labels": [
                verification_choices.get(status, status)
                for status, _ in CarHandling.VERIFICATION_CHOICES
            ],
            "data": [0] * len(CarHandling.VERIFICATION_CHOICES),
        }

        # Update counts based on the retrieved data
        for item in verification_data:
            status = item["verification_status"]
            index = list(verification_choices.keys()).index(status)
            data["data"][index] = item["count"]

        return JsonResponse(data)


class Last5UsersAPIView(APIView):
    def get(self, request, format=None):
        last_5_users = UserAccount.objects.order_by("-id")[:5]
        serializer = CustomUserSerializer(last_5_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Last5VendorsAPIView(APIView):
    def get(self, request, format=None):
        last_5_vendors = VendorProfile.objects.order_by("-id")[:5]
        serializer = VendorModelSerializer(last_5_vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Last5Booking(APIView):
    def get(self, request, format=None):
        last_5_booking = Booking.objects.order_by("-id")[:5]
        serializer = BookingSerializer(last_5_booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlockUserView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(UserAccount, id=user_id)

        # Toggle the block status
        user.is_blocked = not user.is_blocked
        user.save()

        return Response(
            {"status": "success", "is_blocked": user.is_blocked},
            status=status.HTTP_200_OK,
        )


class BlockVendorView(APIView):
    def post(self, request, vendor_id):
        vendor = get_object_or_404(UserAccount, id=vendor_id)

        vendor.is_blocked = not vendor.is_blocked
        vendor.save()

        return Response(
            {"status": "success", "is_blocked": vendor.is_blocked},
            status=status.HTTP_200_OK,
        )
