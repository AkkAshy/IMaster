import sys
import traceback
from django.core.exceptions import ValidationError
from university.models import Room, RoomHistory

print("Начинаем создание склада...")
try:
    # Проверяем, существует ли склад
    if Room.all_objects.filter(is_warehouse=True).exists():
        print("Склад уже существует! Проверяем детали...")
        warehouse = Room.all_objects.get(is_warehouse=True)
        print(f"Склад: {warehouse}, UID: {warehouse.uid}, QR-код: {warehouse.qr_code.url if warehouse.qr_code else 'Не сгенерирован'}")
    else:
        print("Склад не найден, создаём новый...")
        warehouse = Room.objects.create(
            number="WAREHOUSE",
            name="Главный склад оборудования",
            is_warehouse=True,
            is_special=True
        )
        print(f"Склад успешно создан: {warehouse}")
        RoomHistory.objects.create(
            room=warehouse,
            action="Создан склад",
            description="Инициализация главного склада для хранения и распределения оборудования"
        )
        print(f"История создания склада добавлена. QR-код: {warehouse.qr_code.url if warehouse.qr_code else 'Не сгенерирован'}")
except Exception as e:
    print(f"Ошибка при создании склада: {str(e)}")
    print("Полная трассировка ошибки:")
    traceback.print_exc(file=sys.stdout)