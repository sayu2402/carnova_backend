from django.shortcuts import render
from rest_framework.views import APIView
from vendor.models import CarHandling
from rest_framework.response import Response
from rest_framework import status, generics
from .serializer import CarHandlingSerializer
from rest_framework.generics import RetrieveAPIView

# Create your views here.

class CarsList(APIView):
    def get(self, request):
        if request.method == 'GET':
            cars = CarHandling.objects.all().order_by('-created_at')

            # Serialize the data, including the vendor name
            serialized_cars = []
            for car in cars:
                car_data = CarHandlingSerializer(car).data
                car_data['vendor_name'] = car.vendor.user.username
                serialized_cars.append(car_data)

            return Response(serialized_cars, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyCarView(generics.UpdateAPIView):
    queryset = CarHandling.objects.all()
    serializer_class = CarHandlingSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        verification_status = request.data.get('verification_status', None)

        if verification_status not in ['Approved', 'Rejected']:
            return Response({'error': 'Invalid verification status'}, status=status.HTTP_400_BAD_REQUEST)

        instance.verification_status = verification_status
        instance.save()

        # Include vendor_name in the response data
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data['vendor_name'] = instance.vendor.user.username

        return Response(response_data, status=status.HTTP_200_OK)


class CarDetailsView(RetrieveAPIView):
    queryset = CarHandling.objects.all()
    serializer_class = CarHandlingSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data

        # Include vendor_name in the response data
        response_data['vendor_name'] = instance.vendor.user.username

        return Response(response_data, status=status.HTTP_200_OK)