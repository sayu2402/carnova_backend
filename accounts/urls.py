from django.urls import path 
from . import views
from . import emails

from .views import *
from rest_framework_simplejwt.views import (
   
    TokenRefreshView,
)

urlpatterns=[
    path('', GetRoutesView.as_view(), name='get-routes'),
    path('token/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('partnerlogin/', PartnerLoginView.as_view(), name='token_obtain_pair'),
    path('signup/',UserSignupAPI.as_view()),
    path('signup/otp/',emails.generate_otp_and_send_email),
    path('Partnersignup/',PartnerSignupAPI.as_view()),
    path('adminlogin/', AdminLoginView.as_view(), name='admin-login'),
    path('userlist/', UserListView.as_view(), name='userlist'),
    path('vendorlist/', VendorListView.as_view(), name='vendor-list'),
]
