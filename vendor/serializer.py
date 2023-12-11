from rest_framework import serializers
from accounts.models import UserAccount, VendorProfile
from .models import CarHandling



class VendorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
        depth = 2


class VendorProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
        depth = 1


class CarHandlingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarHandling
        fields = '__all__'
