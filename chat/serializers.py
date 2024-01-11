from rest_framework import serializers
from .models import Chat

class MessageSerializer(serializers.ModelSerializer):
       class Meta:
           model = Chat
           fields = ('id', 'sender', 'receiver','message', 'timestamp')
           read_only_fields = ('id', 'timestamp')