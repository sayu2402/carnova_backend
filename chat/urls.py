from django.urls import path
from .views import MessageList

urlpatterns = [
    path('messages/<int:user_id>/', MessageList.as_view(), name='message_list'),
]