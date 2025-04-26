from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUser  # Импортируем кастомный пермишн
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        if not self.request.user.is_admin():
            raise PermissionError("Только администратор может создавать пользователей.")
        serializer.save()
        
    # Этот метод будет отвечать за логику аутентификации
    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Возвращаем успешную авторизацию или токен, если пользователь авторизован
            return super().create(request, *args, **kwargs)
        return Response({"detail": "Unauthorized"}, status=401)
