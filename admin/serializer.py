from rest_framework import serializers
from vendor.models import CarHandling

class CarHandlingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarHandling
        fields = '__all__'
        read_only_fields = ['verification_status']