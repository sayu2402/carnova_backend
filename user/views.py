from django.shortcuts import render
from accounts.models import UserAccount
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.response import Response
from accounts.serializer import CustomUserSerializer, UserProfileUpdateSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .serializer import ChangePasswordSerializer, BookingSerializer
from vendor.serializer import CarHandlingSerializer
from vendor.models import CarHandling
from django.shortcuts import get_object_or_404
from .models import *
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination


# Create your views here

class UserProfileView(APIView):
    def get(self, request, user_id):
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileUpdateSerializer(data=request.data, instance=user_profile, partial=True)

        if serializer.is_valid():
            user_data = serializer.validated_data

            if 'email' in request.data and user_data['email'] is not None:
                user_profile.email = user_data['email']
            if 'username' in user_data and user_data['username'] is not None:
                user_profile.username = user_data['username']
            if 'phone_no' in user_data and user_data['phone_no'] is not None:
                user_profile.phone_no = user_data['phone_no']


            user_profile.save()
            return Response({'message': 'Account updated successfully.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(APIView):
    def post(self, request, user_id):
        user_profile = self.get_object(user_id)

        if not user_profile:
            return Response({'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data.get('current_password')
            new_password = serializer.validated_data.get('new_password')

            if not check_password(current_password, user_profile.password):
                return Response({'message': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            user_profile.password = make_password(new_password)
            user_profile.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, user_id):
        try:
            return UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return None


class CarBrowseView(ListAPIView):
    queryset = CarHandling.objects.filter(verification_status='Approved').order_by('id')
    serializer_class = CarHandlingSerializer
    pagination_class = PageNumberPagination
    page_size = 6


class CarDetailView(APIView):
    def get(self, request, car_id, *args, **kwargs):
        car = get_object_or_404(CarHandling, id=car_id)
        serializer = CarHandlingSerializer(car)

        serialized_data = serializer.data
        serialized_data['vendor_name'] = car.vendor.user.username

        return Response(serialized_data, status=status.HTTP_200_OK)
    

class CarAvailabilityAPIView(APIView):
    def post(self, request, *args, **kwargs):
        car_id = self.kwargs.get('carId')
        pickup_date_str = self.kwargs.get('pickupDate').strip()
        return_date_str = self.kwargs.get('returnDate').strip()

        try:

            pickup_date = timezone.datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
            return_date = timezone.datetime.strptime(return_date_str, '%Y-%m-%d').date()


            car_booking = Booking.objects.filter(
                car_id=car_id,
                return_date__gt=pickup_date,
                pickup_date__lt=return_date,
                is_cancelled=False,
            )

            if car_booking.exists():
                return JsonResponse({"message": "Car not available for the selected dates"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({"message": "Car available for booking"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return JsonResponse({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class UserGoogleLogin(APIView):
    def post(self, request):
        try:
            data = request.data
            if  data:
           
                email = data.get('email')           
                user = UserAccount.objects.filter(email=email).first()

                if user:
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    data = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'username': user.username,
                        'user_id': user.id,
                        'role': user.role,
                        
                    }
                    return Response(data, status=status.HTTP_201_CREATED)

                else:
                    # Handle the case where no user with the specified email is found
                    return Response({'error': 'Authentication failed. User not found or invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response({'error': 'Invalid data. Please provide valid input.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle other exceptions 
            print(e)
            return Response({'error': 'Internal server error. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingList(ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_profile = get_object_or_404(UserProfile, user__id=user_id)
        return Booking.objects.filter(user=user_profile)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)