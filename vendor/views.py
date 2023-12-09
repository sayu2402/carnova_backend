from django.shortcuts import render
from accounts.models import UserAccount
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import VendorModelSerializer, VendorProfileUpdateSerializer
from rest_framework import status
from user.serializer import ChangePasswordSerializer
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.

class VendorProfileView(APIView):
    def get(self, request, user_id):
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorProfileUpdateSerializer(data=request.data, instance=user_profile, partial=True)

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
    

class VendorChangePasswordView(APIView):
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