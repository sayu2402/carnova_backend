from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Chat
from .serializers import MessageSerializer
from accounts.models import UserAccount

class MessageList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(UserAccount, id=user_id)

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
            'authenticated_user_messages': authenticated_user_messages_data
        }, status=status.HTTP_200_OK)
