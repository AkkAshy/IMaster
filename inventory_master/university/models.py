# university/models.py

from django.db import models
from django.core.files import File
import qrcode
import os
from io import BytesIO

class University(models.Model):  # Университет
    name = models.CharField(max_length=255, verbose_name="Название университета")
    address = models.TextField(verbose_name="Адрес")
    logo = models.ImageField(upload_to='university_logos/', null=True, blank=True, verbose_name="Логотип")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Университет"
        verbose_name_plural = "Университеты"



class Building(models.Model):   # Корпус
    university = models.ForeignKey(
        'University',
        on_delete=models.CASCADE,
        related_name='buildings',
        verbose_name="Университет"
    )
    name = models.CharField(max_length=100, verbose_name="Название корпуса")
    address = models.TextField(verbose_name="Адрес корпуса", blank=True)
    photo = models.ImageField(upload_to='building_photos/', null=True, blank=True, verbose_name="Фото корпуса")

    def __str__(self):
        return f"{self.name} — {self.university.name}"

    class Meta:
        verbose_name = "Корпус"
        verbose_name_plural = "Корпуса"



class Faculty(models.Model):    # Факультет
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        related_name='faculties',
        verbose_name="Корпус"
    )
    name = models.CharField(max_length=255, verbose_name="Название факультета")
    photo = models.ImageField(upload_to='faculty_photos/', null=True, blank=True, verbose_name="Фото факультета")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"
        unique_together = ('building', 'name')



class Floor(models.Model): # Этаж
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        related_name='floors',
        verbose_name="Корпус"
    )
    number = models.IntegerField(verbose_name="Номер этажа")
    description = models.TextField(blank=True, verbose_name="Описание (необязательно)")

    def __str__(self):
        return f"Этаж {self.number} — {self.building.name}"

    class Meta:
        verbose_name = "Этаж"
        verbose_name_plural = "Этажи"
        unique_together = ('building', 'number')




class Room(models.Model): # Кабинет
    floor = models.ForeignKey(
        'Floor',
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name="Этаж"
    )
    number = models.CharField(max_length=20, verbose_name="Номер кабинета")
    name = models.CharField(max_length=255, blank=True, verbose_name="Название (если есть)")
    is_special = models.BooleanField(default=False, verbose_name="Специальный кабинет")
    photo = models.ImageField(upload_to='room_photos/', null=True, blank=True, verbose_name="Фото кабинета")
    qr_code = models.ImageField(upload_to='room_qrcodes/', null=True, blank=True, verbose_name="QR-код кабинета")


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала обычное сохранение
        
        if not self.qr_code:  # Если QR-кода ещё нет
            qr = qrcode.make(f"Room ID: {self.id}\nNumber: {self.number}")
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            buffer.seek(0)

            filename = f"room_qr_{self.id}.png"
            self.qr_code.save(filename, File(buffer), save=False)

            super().save(update_fields=['qr_code'])  # Второе сохранение, только для QR

    def __str__(self):
        if self.name:
            return f"{self.number} — {self.name}"
        return f"Кабинет {self.number}"

    class Meta:
        verbose_name = "Кабинет"
        verbose_name_plural = "Кабинеты"
        unique_together = ('floor', 'number')


class Department(models.Model): # Кафедра
    name = models.CharField(max_length=255, verbose_name="Название кафедры")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments", verbose_name="Факультет")

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедры"
        unique_together = ('faculty', 'name')


class RoomHistory(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='histories')
    action = models.CharField(max_length=100)  # например "Разделён"
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
