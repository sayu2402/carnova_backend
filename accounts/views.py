from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from .emails import *
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from accounts.models import UserProfile,VendorProfile,UserAccount



class UserLoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data) 
            
            if serializer.is_valid():
                email = serializer.data['email']  # Prefix with 'user-'
                password = serializer.data['password']
                user = authenticate(email=email, password=password)
                
                if user is None or user.role != 'user' or user.is_blocked:
                    data = {
                        'message': 'Invalid credentials',
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                refresh['role'] = user.role
                refresh['email'] = user.email
                refresh['username'] = user.username
                refresh['phone_no'] = user.phone_no
                refresh['profile_photo'] = str(user.profile_photo) if user.profile_photo else None
                refresh['is_superuser'] = user.is_superuser
                
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': user.username,
                    'role': user.role,
                    'profile_photo': refresh['profile_photo'],
                }
                print("Serialized Data:", data)
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'Invalid input',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Error:", e)
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PartnerLoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            
            if serializer.is_valid():
                email = serializer.data['email']  # Prefix with 'partner-'
                password = serializer.data['password']
                
                user = authenticate(email=email, password=password)
                print("user===============================",user)
                if user is None or user.role != 'partner' :
                    data = {
                        'message': 'invalid credentials',
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                refresh['role'] = user.role
                refresh['email'] = user.email
                refresh['partnername'] = user.username
                
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role':user.role
                    
                }
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

class AdminLoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            # if data.email==is_superuser
            serializer = LoginSerializer(data=data)
            
            if serializer.is_valid() :
                email =   serializer.data['email']  # Prefix with 'partner-'
                password = serializer.data['password']
                print("usemailer",email)
                user = authenticate(email=email, password=password)
                print("user",user)
                if user is None or user.role != 'admin':
                    data = {
                        'message': 'invalid credentials',
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                refresh['role'] = user.role
                refresh['email'] = user.email
                refresh['adminname'] = user.username
                
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role':user.role
                }
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

 
@api_view(['GET'])
def getRoutes(request):
    routes=[
        '/api/token',
        # '/api/token/refresh'
    ]
    return Response(routes)






class UserSignupAPI(APIView):
    def post(self,request):
        print(request.data,"fffffffffffffffffffffff")
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
           
            print(user_data,"ser_data")
            user = UserAccount(
                email = user_data['email'],
                
                role = 'user',
                phone_no = user_data['phone_no'],
                username = user_data['username'],
            )

            user.set_password(user_data['password'] )
            user.save()

            UserProfile.objects.create(user=user)
            return Response({'message':'Account created successfully.'},status=status.HTTP_201_CREATED)
        print("im here",serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



         
class PartnerSignupAPI(APIView):
    def post(self,request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            # user = serializer.save()
           
            user = UserAccount(
                username = user_data['username'],
                
                email = user_data['email'],
                phone_no = user_data['phone_no'],
                role = 'partner'
            )

            user.set_password(user_data['password'] )
            user.save()

            VendorProfile.objects.create(user=user)
            print('partner is created ')
            return Response({'message':'Account created successfully.'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])        
def userlist(request):
    if request.method == 'GET':
        
        data = UserProfile.objects.all()
        
        serializer = UserModelSerializer(data, many=True)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def vendorlist(request):
    if request.method == 'GET':
        
        data = VendorProfile.objects.all()
         
        serializer = VendorModelSerializer(data, many=True)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)