from rest_framework import serializers
from .models import EquipmentType, Equipment, ComputerDetails, MovementHistory, ContractDocument
from university.models import Room
from university.serializers import RoomSerializer


class EquipmentTypeSerializer(serializers.ModelSerializer):
    requires_computer_details = serializers.SerializerMethodField()

    def get_requires_computer_details(self, obj):
        # Считаем, что только тип с name="Компьютер" требует характеристики
        computer_types = ['компьютер']  # Можно расширить, если есть "Ноутбук" и т.д.
        return obj.name.lower() in computer_types

    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'requires_computer_details']
        read_only_fields = ['id']


class ContractDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None

    class Meta:
        model = ContractDocument
        fields = ['id', 'number', 'file', 'file_url', 'created_at']
        read_only_fields = ['id', 'created_at', 'file_url']


class ComputerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerDetails
        fields = [
            'cpu',
            'ram',
            'storage',
            'has_keyboard',
            'has_mouse',
            'monitor_size',
        ]



class EquipmentSerializer(serializers.ModelSerializer):
    contract = ContractDocumentSerializer(read_only=True, allow_null=True)
    computer_details = ComputerDetailsSerializer(required=False)
    type = serializers.PrimaryKeyRelatedField(queryset=EquipmentType.objects.all())
    type_data = EquipmentTypeSerializer(source='type', read_only=True)  # Для name и requires_computer_details
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), allow_null=True, required=False)
    room_data = RoomSerializer(source='room', read_only=True, allow_null=True)  # Для вывода имени комнаты

    class Meta:
        model = Equipment
        fields = [
            'id', 'type', 'type_data', 'room', 'room_data', 'name', 'photo', 'description',
            'is_active', 'contract', 'created_at', 'computer_details', 'inn'
        ]
        read_only_fields = ['created_at']

    def validate(self, data):
        equipment_type = data.get('type')
        computer_details = data.get('computer_details')
        
        # Проверяем, является ли тип "Компьютер"
        is_computer = equipment_type and equipment_type.name.lower() in ['компьютер']
        
        if is_computer and not computer_details:
            raise serializers.ValidationError("Для типа 'Компьютер' требуются компьютерные характеристики.")
        if not is_computer and computer_details:
            raise serializers.ValidationError("Для этого типа оборудования компьютерные характеристики не поддерживаются.")
        
        return data

    def create(self, validated_data):
        computer_data = validated_data.pop('computer_details', None)
        equipment = Equipment.objects.create(**validated_data)
        if computer_data and equipment.type.name.lower() in ['компьютер']:
            ComputerDetails.objects.create(equipment=equipment, **computer_data)
        return equipment

    def update(self, instance, validated_data):
        computer_data = validated_data.pop('computer_details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if computer_data and instance.type.name.lower() in ['компьютер']:
            if hasattr(instance, 'computer_details'):
                for attr, value in computer_data.items():
                    setattr(instance.computer_details, attr, value)
                instance.computer_details.save()
            else:
                ComputerDetails.objects.create(equipment=instance, **computer_data)
        elif computer_data and instance.type.name.lower() not in ['компьютер'] and hasattr(instance, 'computer_details'):
            instance.computer_details.delete()  # Удаляем характеристики, если тип сменился
        return instance



class MovementHistorySerializer(serializers.ModelSerializer):
    equipment = serializers.StringRelatedField()
    from_room = serializers.StringRelatedField()
    to_room = serializers.StringRelatedField()

    class Meta:
        model = MovementHistory
        fields = [
            'id',
            'equipment',
            'from_room',
            'to_room',
            'moved_at',
        ]
