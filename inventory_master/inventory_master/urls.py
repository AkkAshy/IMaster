# project/urls.py
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from user.serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

urlpatterns = [
    path('admin/', admin.site.urls),  # Стандартная Django-админка
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', include('user.urls')),
    path('university/', include('university.urls')),
    path('inventory/', include('inventory.urls')),
    path('custom-admin/', include('custom_admin.urls')),  # Маршруты кастомной админки
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)