from rest_framework import serializers
from vendor.models import *
from accounts.models import *
from .models import *


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, data):
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data


class CarAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarHandling
        fields = ["id", "model", "brand", "availability", "price"]

    availability = serializers.SerializerMethodField()

    def get_availability(self, car):
        return "Available" if car.is_available() else "Not Available"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        depth = 2


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["balance"]
