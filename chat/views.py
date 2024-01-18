from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Chat
from .serializers import MessageSerializer
from accounts.models import *
from user.models import *
from accounts.serializer import *



class MessageList(APIView):
    def get(self, request, user_id, vendor_id):
        # Get user and vendor objects
        user = get_object_or_404(UserAccount, id=user_id)
        vendor = get_object_or_404(UserAccount, id=vendor_id)

        # Get the list of messages between the user and the vendor
        messages = Chat.objects.filter(
            (Q(sender=user, receiver=vendor) | Q(sender=vendor, receiver=user))
        ).order_by('timestamp')

        
        # Serialize the list of messages
        messages_data = MessageSerializer(messages, many=True).data

        return Response({
            'user_id': user.id,
            'vendor_id': vendor.id,
            'user_online_status': user.online_status,
            'vendor_online_status': vendor.online_status,
            'messages': messages_data,
        }, status=status.HTTP_200_OK)
    
    
class MessageListVendor(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(UserAccount, id=user_id)
        vendor = get_object_or_404(UserAccount, id=user_id)

        # Get all unique receivers for the current user
        receivers = set(
            list(Chat.objects.filter(sender=user).values_list('receiver', flat=True)) +
            list(Chat.objects.filter(receiver=user).values_list('sender', flat=True))
        )

        receiver_details = {}
        for receiver_id in receivers:
            receiver = get_object_or_404(UserAccount, id=receiver_id)

            # Get the list of messages with the receiver
            messages = Chat.objects.filter(
                (Q(sender=user, receiver=receiver) | Q(sender=receiver, receiver=user))
            ).order_by('-timestamp')

            # Serialize the list of messages
            messages_data = MessageSerializer(messages, many=True).data

            receiver_details[receiver.username] = {
                'receiver_id': receiver.id,
                'messages': messages_data,
            }

        total_receivers = len(receivers)


        # Additional logic to get the list of messages for the authenticated user
        authenticated_user_messages = Chat.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')

        # Serialize the list of messages for the authenticated user
        authenticated_user_messages_data = MessageSerializer(authenticated_user_messages, many=True).data

        return Response({
            'total_receivers': total_receivers,
            'receiver_details': receiver_details,
            'authenticated_user_messages': authenticated_user_messages_data,
            'vendor_online_status': vendor.online_status,
        }, status=status.HTTP_200_OK)




class MessageLists(APIView):
    def get(self, request, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({'error': 'Invalid user ID format'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(UserAccount, id=user_id)

        receivers = set(
            list(Chat.objects.filter(sender=user).values_list('receiver', flat=True)) +
            list(Chat.objects.filter(receiver=user).values_list('sender', flat=True))
        )

        receiver_details = {}
        for receiver_id in receivers:
            receiver = get_object_or_404(UserAccount, id=receiver_id)

            messages = Chat.objects.filter(
                (Q(sender=user, receiver=receiver) | Q(sender=receiver, receiver=user))
            ).order_by('-timestamp')

            messages_data = MessageSerializer(messages, many=True).data

            receiver_details[receiver.username] = {
                'receiver_id': receiver.id,
                'messages': messages_data,
            }

        total_receivers = len(receivers)

        authenticated_user_messages = Chat.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')

        authenticated_user_messages_data = MessageSerializer(authenticated_user_messages, many=True).data

        user_profile = get_object_or_404(UserProfile, user=user) 
        user_bookings = Booking.objects.filter(user=user_profile)
        corresponding_vendors = VendorProfile.objects.filter(booking__in=user_bookings).distinct()
        vendor_data = VendorModelSerializer(corresponding_vendors, many=True).data


        return Response({
            'total_receivers': total_receivers,
            'receiver_details': receiver_details,
            'authenticated_user_messages': authenticated_user_messages_data,
            'booked_vendors': vendor_data,
        }, status=status.HTTP_200_OK)