from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),  # Пример маршрута для пользователей
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
]
