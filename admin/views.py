from django.shortcuts import render
from rest_framework.generics import ListAPIView
from vendor.models import CarHandling
from rest_framework.response import Response
from rest_framework import status, generics
from .serializer import CarHandlingSerializer
from rest_framework.generics import RetrieveAPIView
from user.models import Booking
from user.serializer import BookingSerializer
from rest_framework.pagination import PageNumberPagination
from admin.tasks import *


# Create your views here.

class CarsList(ListAPIView):
    serializer_class = CarHandlingSerializer
    queryset = CarHandling.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    page_size = 6  # Set your desired page size
    page_size_query_param = 'page_size'
    max_page_size = 100

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Serialize the data, including the vendor name
        serialized_cars = []
        for car in queryset:
            car_data = self.get_serializer(car).data
            car_data['vendor_name'] = car.vendor.user.username
            serialized_cars.append(car_data)

        # Return paginated response
        page = self.paginate_queryset(serialized_cars)
        return self.get_paginated_response(page) if page else Response(serialized_cars)


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
    

class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all().order_by('id')
    serializer_class = BookingSerializer