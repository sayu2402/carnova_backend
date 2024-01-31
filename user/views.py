from accounts.models import UserAccount
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.response import Response
from accounts.serializer import CustomUserSerializer, UserProfileUpdateSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .serializer import *
from vendor.serializer import CarHandlingSerializer
from vendor.models import CarHandling
from django.shortcuts import get_object_or_404
from .models import *
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
import logging
from datetime import datetime


# Create your views here


class UserProfileView(APIView):
    def get(self, request, user_id):
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return Response(
                {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
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

        serializer = UserProfileUpdateSerializer(
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


class ChangePasswordView(APIView):
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


class CarBrowseView(ListAPIView):
    queryset = CarHandling.objects.filter(verification_status="Approved").order_by(
        "-id"
    )
    serializer_class = CarHandlingSerializer
    pagination_class = PageNumberPagination
    page_size = 6


class CarDetailView(APIView):
    def get(self, request, car_id, *args, **kwargs):
        car = get_object_or_404(CarHandling, id=car_id)
        serializer = CarHandlingSerializer(car)

        serialized_data = serializer.data
        serialized_data["vendor_name"] = car.vendor.user.username

        return Response(serialized_data, status=status.HTTP_200_OK)


class CarAvailabilityAPIView(APIView):
    def post(self, request, *args, **kwargs):
        car_id = self.kwargs.get("carId")
        user_id = self.kwargs.get("userId")

        print(user_id, "_________________")

        customuser_obj = UserAccount.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=customuser_obj)
        
        pickup_date_str = self.kwargs.get("pickupDate").strip()
        return_date_str = self.kwargs.get("returnDate").strip()

        try:
            pickup_date = timezone.datetime.strptime(pickup_date_str, "%Y-%m-%d").date()
            return_date = timezone.datetime.strptime(return_date_str, "%Y-%m-%d").date()


            id_card_exists = IDCard.objects.filter(user_profile=user_profile).exists()

            if not id_card_exists:
                return Response(
                    {
                        "message": "ID card not found. Upload your ID card before booking.",
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "id_card_exists": False,
                    }
                )

            car_booking = Booking.objects.filter(
                car_id=car_id,
                return_date__gt=pickup_date,
                pickup_date__lt=return_date,
                is_cancelled=False,
            )

            if car_booking.exists():
                return JsonResponse(
                    {"message": "Car not available for the selected dates"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return JsonResponse(
                    {"message": "Car available for booking"}, status=status.HTTP_200_OK
                )

        except Exception as e:
            print(e)
            return JsonResponse(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserGoogleLogin(APIView):
    def post(self, request):
        try:
            data = request.data
            if data:
                email = data.get("email")
                user = UserAccount.objects.filter(email=email).first()

                if user:
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    data = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "username": user.username,
                        "user_id": user.id,
                        "role": user.role,
                    }
                    return Response(data, status=status.HTTP_201_CREATED)

                else:
                    # Handle the case where no user with the specified email is found
                    return Response(
                        {
                            "error": "Authentication failed. User not found or invalid credentials."
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

            else:
                return Response(
                    {"error": "Invalid data. Please provide valid input."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            # Handle other exceptions
            print(e)
            return Response(
                {"error": "Internal server error. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BookingList(ListAPIView):
    serializer_class = BookingSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user_profile = get_object_or_404(UserProfile, user__id=user_id)
        return Booking.objects.filter(user=user_profile).order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CancelOrder(APIView):
    def post(self, request, user_id, booking_id, *args, **kwargs):
        try:
            booking = get_object_or_404(Booking, id=booking_id, user__user__id=user_id)

            wallet, created = Wallet.objects.get_or_create(user=booking.user)
            wallet.balance += booking.total_amount
            wallet.save()

            booking.is_cancelled = True
            booking.save()

            transaction = Transcation.objects.get(booking=booking)
            transaction.vendor_share -= int(booking.total_amount * 0.7)
            transaction.company_share -= int(booking.total_amount * 0.3)
            transaction.save()

            return Response(
                {"message": "canceled successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WalletMoney(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        user = UserAccount.objects.get(id=user_id)
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        try:
            # Try to get the existing wallet
            wallet = Wallet.objects.get(user=user_profile)
        except Wallet.DoesNotExist:
            # If the wallet doesn't exist, create a new one
            wallet = Wallet.objects.create(user=user_profile)

        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchByLocation(ListAPIView):
    serializer_class = CarHandlingSerializer

    def validate_date(self, date_str):
        try:
            return timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    def check_car_availability_by_dates(self, car_id, pickup_date, return_date):
        return Booking.objects.filter(
            car_id=car_id,
            return_date__gt=pickup_date,
            pickup_date__lt=return_date,
            is_cancelled=False,
        ).exists()

    def check_car_availability_by_location(self, partial_location):
        normalized_partial_location = partial_location.lower()
        return CarHandling.objects.filter(
            location__icontains=normalized_partial_location, is_available=True
        ).exists()

    def post(self, request, *args, **kwargs):
        car_id = self.request.data.get("carId")
        pickup_date_str = self.request.data.get("pickupDate").strip()
        return_date_str = self.request.data.get("returnDate").strip()
        partial_location = self.request.data.get("location", "").strip()

        try:
            pickup_date = self.validate_date(pickup_date_str)
            return_date = self.validate_date(return_date_str)

            if not pickup_date or not return_date:
                return Response(
                    {"message": "Invalid date format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if self.check_car_availability_by_dates(car_id, pickup_date, return_date):
                return Response(
                    {"message": "Car not available for the selected dates"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if self.check_car_availability_by_location(partial_location):
                matching_cars = CarHandling.objects.filter(
                    location__icontains=partial_location, is_available=True
                )
                serializer = self.get_serializer(matching_cars, many=True)
                return Response(
                    {
                        "message": "Cars available at the location",
                        "matching_cars": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "No cars available at the matched location"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return Response(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class LatestAddedCars(ListAPIView):
    queryset = CarHandling.objects.filter(verification_status="Approved").order_by(
        "-id"
    )[:4]
    serializer_class = CarHandlingSerializer


class WalletPaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get("userId")

        try:
            car_id = self.kwargs.get("carId")
            pickup_date = self.kwargs.get("pickupDate").strip()
            return_date = self.kwargs.get("returnDate").strip()
            user_id = self.kwargs.get("userId")

            car = CarHandling.objects.get(id=car_id)
            customuser_obj = UserAccount.objects.get(id=user_id)
            user_profile = UserProfile.objects.get(user=customuser_obj)

            pickup_datetime = datetime.strptime(pickup_date, "%Y-%m-%d")
            return_datetime = datetime.strptime(return_date, "%Y-%m-%d")

            no_ofdays = (return_datetime - pickup_datetime).days + 1

            daily_rate = car.price
            total_amount = daily_rate * no_ofdays

            wallet = Wallet.objects.get(user=user_profile)
            current_balance = wallet.balance

            if user_profile.user.is_blocked:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Blocked user can't perform wallet transactions",
                    "is_blocked": True,
                }
                return Response(response)

            id_card_exists = IDCard.objects.filter(user_profile=user_profile).exists()

            if not id_card_exists:
                return Response(
                    {
                        "message": "ID card not found. Upload your ID card before booking.",
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "id_card_exists": False,
                    }
                )

            # Assuming request.data contains the payment amount
            payment_amount = request.data.get("amount")

            if payment_amount is not None and payment_amount > 0:
                # Check if the wallet has sufficient balance
                if wallet.balance >= payment_amount:
                    # Deduct the amount from the user's wallet
                    wallet.balance -= payment_amount
                    wallet.save()

                    booking_obj = Booking.objects.create(
                        car=car,
                        user=user_profile,
                        pickup_date=pickup_date,
                        return_date=return_date,
                        total_amount=total_amount,
                        vendor=car.vendor,
                    )

                    Transcation.objects.create(
                        booking=booking_obj,
                        user=user_profile,
                        vendor=car.vendor,
                        vendor_share=0.7 * float(total_amount),
                        company_share=0.3 * float(total_amount),
                    )

                    response = {
                        "status_code": status.HTTP_200_OK,
                        "message": "Payment successful",
                        "wallet_balance": wallet.balance,
                        "current_balance": current_balance,
                    }
                else:
                    response = {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "Insufficient funds in the wallet",
                    }
            else:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid payment amount",
                }

            return Response(response)

        except UserProfile.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "User not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Wallet.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Wallet not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Bad request",
                "error": str(e),
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class IDCardUploadView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        user_profile = get_object_or_404(UserProfile, user__id=user_id)

        serializer = IDCardSerializer(data=request.data)

        if serializer.is_valid():
            id_card = serializer.save(user_profile=user_profile)
            return Response(
                {"message": "ID card uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IDCardView(APIView):
    def get(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            id_card = IDCard.objects.get(user_profile=user_profile)
            serializer = IDCardSerializer(id_card)
            return Response(serializer.data)
        except IDCard.DoesNotExist:
            return Response(
                {"message": "ID card not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = IDCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user_profile)
            return Response(
                {"message": "ID card uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckIDCardView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            id_card_exists = IDCard.objects.filter(user_profile=user_profile).exists()

            response_data = {"id_card_exists": id_card_exists}

            return Response(response_data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
