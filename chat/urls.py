from django.urls import path
from .views import *

urlpatterns = [
    path('messages/<int:user_id>/<int:vendor_id>/', MessageList.as_view(), name='user_vendor_messages'),
    path('booked-vendors/<int:user_id>/', MessageListVendor.as_view(), name='user_booked_vendors_api'),
    path('message/<int:user_id>/', MessageLists.as_view(), name='message_list'),
]