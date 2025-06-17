from rest_framework import serializers
from .models import (EquipmentType, Equipment, ComputerDetails,
                     MovementHistory, ContractDocument, ComputerSpecification,
                     RouterSpecification, ExtenderSpecification, TVSpecification, PrinterSpecification,
                     RouterChar, ExtenderChar, TVChar, PrinterChar,
                     NotebookChar, NotebookSpecification, MonoblokChar, MonoblokSpecification,
                     ProjectorChar, ProjectorSpecification, WhiteboardChar, WhiteboardSpecification,
                     Repair, Disposal, Disk, DiskSpecification, MonitorChar, MonitorSpecification,
                     GPU, GPUSpecification
                     )
# Базовый сериализатор для характеристик
class BaseCharacteristicSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    equipment_id = serializers.IntegerField(source='equipment.id', read_only=True)
    equipment_type = serializers.CharField(source='equipment.equipment_type', read_only=True)

    class Meta:
        fields = '__all__'

# Сериализаторы для всех типов характеристик
class PrinterCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = PrinterChar  # Замените your_app_name на реальное название
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.model} ({obj.specification.serial_number})"
        return None

class ExtenderCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = ExtenderChar
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.ports} портов, {obj.specification.length}"
        return None

class RouterCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = RouterChar
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.model} ({obj.specification.serial_number})"
        return None

class TVCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = TVChar
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.model} ({obj.specification.screen_size})"
        return None

class NotebookCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = NotebookChar
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.cpu}, {obj.specification.ram}"
        return None

class MonoblokCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = MonoblokChar
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.cpu}, {obj.specification.ram}"
        return None

class ProjectorCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = ProjectorChar
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.model} ({obj.specification.lumens} люмен)"
        return None

class WhiteboardCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = WhiteboardChar
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.model} ({obj.specification.screen_size}\")"
        return None

class MonitorCharSerializer(BaseCharacteristicSerializer):
    specification_name = serializers.SerializerMethodField()

    class Meta:
        model = MonitorChar
        fields = '__all__'

    def get_specification_name(self, obj):
        if obj.specification:
            return f"{obj.specification.model} ({obj.specification.screen_size}\")"
        return None

# Сериализатор для поиска оборудования
class EquipmentSearchSerializer(serializers.Serializer):
    equipment_type = serializers.CharField(help_text="Тип оборудования для поиска")

    # Общие поля для поиска
    model = serializers.CharField(required=False, help_text="Модель")
    serial_number = serializers.CharField(required=False, help_text="Серийный номер")

    # Для принтеров
    color = serializers.BooleanField(required=False, help_text="Цветной принтер")
    duplex = serializers.BooleanField(required=False, help_text="Дуплексный принтер")

    # Для компьютеров/ноутбуков/моноблоков
    cpu = serializers.CharField(required=False, help_text="Процессор")
    ram = serializers.CharField(required=False, help_text="Оперативная память")
    monitor_size = serializers.CharField(required=False, help_text="Размер монитора")

    # Для роутеров/удлинителей
    ports = serializers.IntegerField(required=False, help_text="Количество портов")
    wifi_standart = serializers.CharField(required=False, help_text="Стандарт Wi-Fi")
    length = serializers.CharField(required=False, help_text="Длина кабеля")

    # Для телевизоров/досок
    screen_size = serializers.CharField(required=False, help_text="Размер экрана")

    # Для проекторов
    lumens = serializers.IntegerField(required=False, help_text="Яркость в люменах")
    resolution = serializers.CharField(required=False, help_text="Разрешение")
    throw_type = serializers.CharField(required=False, help_text="Тип проекции")

    # Для досок
    touch_type = serializers.CharField(required=False, help_text="Тип сенсора")

    # Для моноблоков
    has_keyboard = serializers.BooleanField(required=False, help_text="Есть клавиатура")
    has_mouse = serializers.BooleanField(required=False, help_text="Есть мышь")

    # Для мониторов
    model = serializers.CharField(required=False, help_text="Модель монитора")
    serial_number = serializers.CharField(required=False, help_text="Серийный номер")
    screen_size = serializers.CharField(required=False, help_text="Размер экрана")
    resolution = serializers.CharField(required=False, help_text="Разрешение")
    refresh_rate = serializers.IntegerField(required=False, help_text="Частота обновления (Гц)")

# Обобщенный сериализатор для результатов поиска
class EquipmentSearchResultSerializer(serializers.Serializer):
    equipment_id = serializers.IntegerField()
    equipment_name = serializers.CharField()
    equipment_type = serializers.CharField()
    characteristics = serializers.DictField()
    specification_name = serializers.CharField(allow_null=True)
    author = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField(allow_null=True)