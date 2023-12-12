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

    def create(self, validated_data):
        vendor_data = validated_data.pop('vendor', None)

        car_handling = CarHandling.objects.create(**validated_data)

        if vendor_data is not None:
            car_handling.vendor = vendor_data
            car_handling.save()

        return car_handling