from rest_framework import serializers
from accounts.models import UserAccount



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