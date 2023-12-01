from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('accounts.urls')),
    # path('api-auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # path('auth/', include('social_django.urls', namespace='social')),
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
