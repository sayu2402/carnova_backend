from django.shortcuts import get_object_or_404
from accounts.models import UserAccount, VendorProfile
from rest_framework.views import APIView
from django.views import View
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.http import JsonResponse
from .serializer import *
from rest_framework import generics, status
from django.db.models import Count
from user.serializer import ChangePasswordSerializer, BookingSerializer
from django.contrib.auth.hashers import make_password, check_password
from .models import CarHandling
from user.models import Booking, Transcation
from django.db.models import Sum
from django.utils import timezone
from rest_framework.exceptions import NotFound


# Create your views here.


class VendorProfileView(APIView):
    def get(self, request, user_id):
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return Response(
                {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = VendorModelSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VendorProfileUpdateView(APIView):
    def get_object(self, user_id):
        try:
            return UserAccount.objects.get(id=user_id)

        except UserAccount.DoesNotExist:
            return None

    def post(self, request, user_id):
        user_profile = self.get_object(user_id)

        if not user_profile:
            return Response(
                {"message": "User profile not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = VendorProfileUpdateSerializer(
            data=request.data, instance=user_profile, partial=True
        )

        if serializer.is_valid():
            user_data = serializer.validated_data

            if "email" in request.data and user_data["email"] is not None:
                user_profile.email = user_data["email"]
            if "username" in user_data and user_data["username"] is not None:
                user_profile.username = user_data["username"]
            if "phone_no" in user_data and user_data["phone_no"] is not None:
                user_profile.phone_no = user_data["phone_no"]

            user_profile.save()
            return Response(
                {"message": "Account updated successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorChangePasswordView(APIView):
    def post(self, request, user_id):
        user_profile = self.get_object(user_id)

        if not user_profile:
            return Response(
                {"message": "User profile not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")

            if not check_password(current_password, user_profile.password):
                return Response(
                    {"message": "Current password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_profile.password = make_password(new_password)
            user_profile.save()
            return Response(
                {"message": "Password updated successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, user_id):
        try:
            return UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return None


class AddCarView(APIView):
    def post(self, request, vendor_id):
        vendor = get_object_or_404(VendorProfile, user__id=vendor_id)
        vendor_blk = get_object_or_404(UserAccount, id=vendor_id)
        vendor_name = vendor.user.username

        if vendor_blk.is_blocked:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Blocked user cant add cars",
                "is_blocked": True,
            }
            return Response(response)

        # Create a mutable copy of request.data
        mutable_data = request.data.copy()

        # Add 'vendor_name' and 'vendor' to the mutable data
        mutable_data["vendor_name"] = vendor_name
        mutable_data["vendor"] = vendor.id

        # Create a serializer with the mutable data
        serializer = CarHandlingSerializer(data=mutable_data)

        if serializer.is_valid():
            serializer.save(vendor_id=vendor.id)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorCarDetailsView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request, vendor_id):
        cars = CarHandling.objects.filter(vendor__user__id=vendor_id)

        # Apply pagination
        paginator = self.pagination_class()
        paginated_cars = paginator.paginate_queryset(cars, request)

        serializer = CarHandlingSerializer(paginated_cars, many=True)
        return paginator.get_paginated_response(serializer.data)


class EditCarDetailsView(APIView):
    def get(self, request, car_id):
        car = get_object_or_404(CarHandling, id=car_id)
        serializer = CarHandlingSerializer(car)
        return Response(serializer.data)

    def patch(self, request, car_id):
        car = get_object_or_404(CarHandling, id=car_id)
        serializer = CarHandlingSerializer(car, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingListView(APIView):
    def get(self, request, id):
        try:
            vendor = VendorProfile.objects.get(user_id=id)
            bookings = Booking.objects.filter(vendor=vendor)

            serialized_bookings = BookingSerializer(bookings, many=True)

            return Response(serialized_bookings.data, status=status.HTTP_200_OK)
        except VendorProfile.DoesNotExist:
            return Response(
                {"detail": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UpdateBookingStatusView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

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


class VendorStatsAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            vendor = get_object_or_404(VendorProfile, user_id=user_id)
            total_revenue = (
                Transcation.objects.filter(vendor=vendor).aggregate(
                    Sum("vendor_share")
                )["vendor_share__sum"]
                or 0
            )
            bookings_count = Booking.objects.filter(vendor=vendor).count()
            total_cars = CarHandling.objects.filter(vendor=vendor).count()

            # Calculate monthly revenue for the current month for the specific vendor
            current_month = timezone.now().month
            monthly_revenue = (
                Transcation.objects.filter(
                    vendor=vendor, transaction_date__month=current_month
                ).aggregate(Sum("vendor_share"))["vendor_share__sum"]
                or 0
            )

            data = {
                "totalRevenue": total_revenue,
                "bookings": bookings_count,
                "totalCars": total_cars,
                "monthlyRevenue": monthly_revenue,
            }

            return Response(data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PieChartVendorDataView(View):
    def get(self, request, vendor_id, *args, **kwargs):
        vendor = get_object_or_404(VendorProfile, user_id=vendor_id)

        verification_choices = dict(CarHandling.VERIFICATION_CHOICES)
        verification_data = (
            CarHandling.objects.filter(vendor=vendor)
            .values("verification_status")
            .annotate(count=Count("verification_status"))
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
