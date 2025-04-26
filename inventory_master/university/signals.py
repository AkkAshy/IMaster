from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Room
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import qrcode

@receiver(post_save, sender=Room)
def generate_qr_code(sender, instance, created, **kwargs):
    """
    Генерация QR-кода для кабинета после его сохранения
    """
    if created or instance.qr_code is None:  # Генерируем QR-код только при создании нового объекта или если он отсутствует
        qr_code_file = generate_qr_code_for_room(instance)
        instance.qr_code = qr_code_file
        instance.save()

def generate_qr_code_for_room(room):
    """
    Функция для генерации QR-кода для кабинета
    """
    qr = qrcode.make(f"Room: {room.number}, {room.name}, Floor: {room.floor.number}")

    # Сохранение QR-кода как изображения в память
    img_io = BytesIO()
    qr.save(img_io, format='PNG')
    img_io.seek(0)

    # Конвертация в файл для сохранения
    qr_code_file = InMemoryUploadedFile(img_io, None, f"qr_{room.number}.png", 'image/png', img_io.tell(), None)
    
    return qr_code_file
