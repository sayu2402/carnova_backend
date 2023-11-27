from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError, ImageField
from accounts.models import UserProfile,VendorProfile,UserAccount


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = UserAccount

 
class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAccount
        fields = ('email','username','phone_no','password')
        extra_kwargs = {
            'password':{'write_only':True}
        }


class EmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
        depth=2
       

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  
        depth = 2