from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        MANAGER = 'manager', 'Менеджер'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MANAGER,
        verbose_name="Роль"
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефонный номер")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="Фото профиля")

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_manager(self):
        return self.role == self.Role.MANAGER

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"
