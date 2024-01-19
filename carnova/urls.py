from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import GoogleLogin

urlpatterns = [
    path("api/", include("accounts.urls")),
    path("api/user/", include("user.urls")),
    path("api/vendor/", include("vendor.urls")),
    path("api/admin/", include("admin.urls")),
    path("api/razorpay/", include("user.api_razorpay.urls")),
    path("api/chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
