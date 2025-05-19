# from rest_framework import serializers
# from .models import (EquipmentType, Equipment, ComputerDetails,
#                      MovementHistory, ContractDocument, ComputerSpecification,
#                      RouterChar, ExtenderChar, TVChar, PrinterChar,
#                      RouterSpecification, ExtenderSpecification, TVSpecification, PrinterSpecification,
#                      RouterChar, ExtenderChar, TVChar, PrinterChar,
#                      NotebookChar, NotebookSpecification, MonoblokChar, MonoblokSpecification,
#                      ProjectorChar, ProjectorSpecification, WhiteboardChar, WhiteboardSpecification)
# from university.models import Room
# from university.serializers import RoomSerializer
# from user.serializers import UserSerializer

# from io import BytesIO
# import qrcode
# from django.core.files import File
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class EquipmentTypeSerializer(serializers.ModelSerializer):
#     requires_computer_details = serializers.SerializerMethodField()

#     def get_requires_computer_details(self, obj):
#         # Считаем, что только тип с name="Компьютер" требует характеристики
#         computer_types = ['компьютер', 'ноутбук', 'моноблок']
#         return obj.name.lower() in computer_types

#     class Meta:
#         model = EquipmentType
#         fields = ['id', 'name', 'requires_computer_details']
#         read_only_fields = ['id']


# class ContractDocumentSerializer(serializers.ModelSerializer):
#     file_url = serializers.SerializerMethodField()

#     def get_file_url(self, obj):
#         if obj.file:
#             return self.context['request'].build_absolute_uri(obj.file.url)
#         return None

#     class Meta:
#         model = ContractDocument
#         fields = ['id', 'number', 'file', 'file_url', 'created_at']
#         read_only_fields = ['id', 'created_at', 'file_url']


# class ComputerDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ComputerDetails
#         fields = [
#             'cpu',
#             'ram',
#             'storage',
#             'has_keyboard',
#             'has_mouse',
#             'monitor_size',
#         ]


# class ComputerSpecificationSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#     author_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         write_only=True,
#         required=False,
#         allow_null=True,
#         source='author'
#     )
#     class Meta:
#         model = ComputerSpecification
#         fields = [
#             'id', 'cpu', 'ram', 'storage', 'has_keyboard', 'has_mouse',
#             'monitor_size', 'created_at', 'uid', 'author', 'author_id'
#         ]
#         read_only_fields = ['created_at', 'uid', 'author', 'author_id']



# class PrinterCharSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PrinterChar
#         fields = '__all__'
#         read_only_fields = ('author', 'created_at', 'updated_at')


# class ExtenderCharSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExtenderChar
#         fields = '__all__'
#         read_only_fields = ('author', 'created_at', 'updated_at')


# class RouterCharSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RouterChar
#         fields = '__all__'
#         read_only_fields = ('author', 'created_at', 'updated_at')


# class TVCharSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TVChar
#         fields = '__all__'
#         read_only_fields = ('author', 'created_at', 'updated_at')


# class PrinterSpecificationSerializer(serializers.ModelSerializer):
#     def get_queryset(self):
#         user = self.context['request'].user
#         if user.is_authenticated:
#             return PrinterSpecification.objects.filter(author=user)
#         return PrinterSpecification.objects.none()

#     class Meta:
#         model = PrinterSpecification
#         fields = ['id', 'model', 'color', 'duplex', 'author', 'created_at', 'updated_at']

# class ExtenderSpecificationSerializer(serializers.ModelSerializer):
#     length = serializers.FloatField()

#     def get_queryset(self):
#         user = self.context['request'].user
#         if user.is_authenticated:
#             return ExtenderSpecification.objects.filter(author=user)
#         return ExtenderSpecification.objects.none()

#     class Meta:
#         model = ExtenderSpecification
#         fields = ['id', 'ports', 'length', 'author', 'created_at', 'updated_at']

# class RouterSpecificationSerializer(serializers.ModelSerializer):
#     WIFI_STANDARDS = [
#         ('802.11n', 'Wi-Fi 4'),
#         ('802.11ac', 'Wi-Fi 5'),
#         ('802.11ax', 'Wi-Fi 6'),
#     ]
#     wifi_standart = serializers.ChoiceField(choices=WIFI_STANDARDS)

#     def get_queryset(self):
#         user = self.context['request'].user
#         if user.is_authenticated:
#             return RouterSpecification.objects.filter(author=user)
#         return RouterSpecification.objects.none()

#     class Meta:
#         model = RouterSpecification
#         fields = ['id', 'model', 'ports', 'wifi_standart', 'author', 'created_at', 'updated_at']

# class TVSpecificationSerializer(serializers.ModelSerializer):
#     screen_size = serializers.IntegerField()

#     def get_queryset(self):
#         user = self.context['request'].user
#         if user.is_authenticated:
#             return TVSpecification.objects.filter(author=user)
#         return TVSpecification.objects.none()

#     class Meta:
#         model = TVSpecification
#         fields = ['id', 'model', 'screen_size', 'author', 'created_at', 'updated_at']



# class EquipmentSerializer(serializers.ModelSerializer):
#     COMPUTER_TYPES = {'компьютер', 'ноутбук', 'моноблок'}
#     PRINTER_TYPES = {'принтер', 'мфу'}
#     EXTENDER_TYPES = {'удлинитель', 'сетевой фильтр'}
#     ROUTER_TYPES = {'роутер'}
#     TV_TYPES = {'телевизор'}

#     # Существующие поля (не тронуты)
#     contract = ContractDocumentSerializer(read_only=True, allow_null=True)
#     computer_details = ComputerDetailsSerializer(required=False, allow_null=True)
#     computer_specification_id = serializers.PrimaryKeyRelatedField(
#         queryset=ComputerSpecification.objects.all(),
#         required=False,
#         allow_null=True,
#         write_only=True,
#         help_text="ID шаблона компьютерной спецификации для автозаполнения характеристик"
#     )
#     computer_specification_data = ComputerSpecificationSerializer(source='computer_details', read_only=True, allow_null=True)
#     type = serializers.PrimaryKeyRelatedField(queryset=EquipmentType.objects.all())
#     type_data = EquipmentTypeSerializer(source='type', read_only=True)
#     room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), allow_null=True, required=False)
#     room_data = RoomSerializer(source='room', read_only=True, allow_null=True)
#     qr_code_url = serializers.SerializerMethodField()
#     author = UserSerializer(read_only=True)
#     author_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         write_only=True,
#         required=False,
#         allow_null=True,
#         source='author'
#     )

#     # Новые поля для характеристик
#     printer_char = PrinterCharSerializer(required=False, allow_null=True)
#     extender_char = ExtenderCharSerializer(required=False, allow_null=True)
#     router_char = RouterCharSerializer(required=False, allow_null=True)
#     tv_char = TVCharSerializer(required=False, allow_null=True)

#     # Новые поля для спецификаций
#     printer_specification_id = serializers.PrimaryKeyRelatedField(
#         queryset=PrinterSpecification.objects.all(),
#         required=False,
#         allow_null=True,
#         write_only=True,
#         help_text="ID шаблона спецификации принтера для автозаполнения характеристик"
#     )
#     extender_specification_id = serializers.PrimaryKeyRelatedField(
#         queryset=ExtenderSpecification.objects.all(),
#         required=False,
#         allow_null=True,
#         write_only=True,
#         help_text="ID шаблона спецификации удлинителя для автозаполнения характеристик"
#     )
#     router_specification_id = serializers.PrimaryKeyRelatedField(
#         queryset=RouterSpecification.objects.all(),
#         required=False,
#         allow_null=True,
#         write_only=True,
#         help_text="ID шаблона спецификации роутера для автозаполнения характеристик"
#     )
#     tv_specification_id = serializers.PrimaryKeyRelatedField(
#         queryset=TVSpecification.objects.all(),
#         required=False,
#         allow_null=True,
#         write_only=True,
#         help_text="ID шаблона спецификации телевизора для автозаполнения характеристик"
#     )

#     # Поля для отображения данных спецификаций
#     printer_specification_data = PrinterSpecificationSerializer(source='printer_char', read_only=True, allow_null=True)
#     extender_specification_data = ExtenderSpecificationSerializer(source='extender_char', read_only=True, allow_null=True)
#     router_specification_data = RouterSpecificationSerializer(source='router_char', read_only=True, allow_null=True)
#     tv_specification_data = TVSpecificationSerializer(source='tv_char', read_only=True, allow_null=True)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             # Фильтрация шаблонов по автору
#             self.fields['computer_specification_id'].queryset = ComputerSpecification.objects.filter(author=request.user)
#             self.fields['printer_specification_id'].queryset = PrinterSpecification.objects.filter(author=request.user)
#             self.fields['extender_specification_id'].queryset = ExtenderSpecification.objects.filter(author=request.user)
#             self.fields['router_specification_id'].queryset = RouterSpecification.objects.filter(author=request.user)
#             self.fields['tv_specification_id'].queryset = TVSpecification.objects.filter(author=request.user)
#         else:
#             # Для анонимных пользователей — пустой queryset
#             self.fields['computer_specification_id'].queryset = ComputerSpecification.objects.none()
#             self.fields['printer_specification_id'].queryset = PrinterSpecification.objects.none()
#             self.fields['extender_specification_id'].queryset = ExtenderSpecification.objects.none()
#             self.fields['router_specification_id'].queryset = RouterSpecification.objects.none()
#             self.fields['tv_specification_id'].queryset = TVSpecification.objects.none()

#     class Meta:
#         model = Equipment
#         fields = [
#             'id', 'type', 'type_data', 'room', 'room_data', 'name', 'photo', 'description',
#             'is_active', 'contract', 'created_at', 'computer_details', 'computer_specification_id',
#             'computer_specification_data', 'printer_char', 'printer_specification_id',
#             'printer_specification_data', 'extender_char', 'extender_specification_id',
#             'extender_specification_data', 'router_char', 'router_specification_id',
#             'router_specification_data', 'tv_char', 'tv_specification_id',
#             'tv_specification_data', 'status', 'qr_code_url', 'uid', 'author', 'author_id', 'inn'
#         ]
#         read_only_fields = ['created_at', 'uid', 'author']

#     def get_qr_code_url(self, obj):
#         if obj.qr_code:
#             return obj.qr_code.url
#         return None

#     def validate(self, data):
#         equipment_type = data.get('type')
#         if not equipment_type:
#             raise serializers.ValidationError("Поле type обязательно.")

#         type_name = equipment_type.name.lower()
#         computer_details = data.get('computer_details')
#         computer_specification_id = data.get('computer_specification_id')
#         printer_char = data.get('printer_char')
#         printer_specification_id = data.get('printer_specification_id')
#         extender_char = data.get('extender_char')
#         extender_specification_id = data.get('extender_specification_id')
#         router_char = data.get('router_char')
#         router_specification_id = data.get('router_specification_id')
#         tv_char = data.get('tv_char')
#         tv_specification_id = data.get('tv_specification_id')

#         # Проверка для компьютеров (оставлена без изменений)
#         is_computer = type_name in self.COMPUTER_TYPES
#         if is_computer and computer_details and computer_specification_id:
#             raise serializers.ValidationError(
#                 "Укажите либо computer_details, либо computer_specification_id, но не оба."
#             )
#         if not is_computer and (computer_details or computer_specification_id):
#             raise serializers.ValidationError(
#                 "Для этого типа оборудования компьютерные характеристики не поддерживаются."
#             )

#         # Проверка для принтеров
#         is_printer = type_name in self.PRINTER_TYPES
#         if is_printer:
#             if printer_char and printer_specification_id:
#                 raise serializers.ValidationError(
#                     "Укажите либо printer_char, либо printer_specification_id, но не оба."
#                 )
#             if not printer_char and not printer_specification_id:
#                 raise serializers.ValidationError(
#                     "Для принтеров требуется указать printer_char или printer_specification_id."
#                 )
#         elif printer_char or printer_specification_id:
#             raise serializers.ValidationError(
#                 "Характеристики принтеров поддерживаются только для принтеров."
#             )

#         # Проверка для удлинителей
#         is_extender = type_name in self.EXTENDER_TYPES
#         if is_extender:
#             if extender_char and extender_specification_id:
#                 raise serializers.ValidationError(
#                     "Укажите либо extender_char, либо extender_specification_id, но не оба."
#                 )
#             if not extender_char and not extender_specification_id:
#                 raise serializers.ValidationError(
#                     "Для удлинителей требуется указать extender_char или extender_specification_id."
#                 )
#         elif extender_char or extender_specification_id:
#             raise serializers.ValidationError(
#                 "Характеристики удлинителей поддерживаются только для удлинителей."
#             )

#         # Проверка для роутеров
#         is_router = type_name in self.ROUTER_TYPES
#         if is_router:
#             if router_char and router_specification_id:
#                 raise serializers.ValidationError(
#                     "Укажите либо router_char, либо router_specification_id, но не оба."
#                 )
#             if not router_char and not router_specification_id:
#                 raise serializers.ValidationError(
#                     "Для роутеров требуется указать router_char или router_specification_id."
#                 )
#         elif router_char or router_specification_id:
#             raise serializers.ValidationError(
#                 "Характеристики роутеров поддерживаются только для роутеров."
#             )

#         # Проверка для телевизоров
#         is_tv = type_name in self.TV_TYPES
#         if is_tv:
#             if tv_char and tv_specification_id:
#                 raise serializers.ValidationError(
#                     "Укажите либо tv_char, либо tv_specification_id, но не оба."
#                 )
#             if not tv_char and not tv_specification_id:
#                 raise serializers.ValidationError(
#                     "Для телевизоров требуется указать tv_char или tv_specification_id."
#                 )
#         elif tv_char or tv_specification_id:
#             raise serializers.ValidationError(
#                 "Характеристики телевизоров поддерживаются только для телевизоров."
#             )

#         return data

#     def create(self, validated_data):
#         # Существующие данные
#         computer_details_data = validated_data.pop('computer_details', None)
#         computer_specification = validated_data.pop('computer_specification_id', None)
#         # Новые данные
#         printer_char_data = validated_data.pop('printer_char', None)
#         printer_specification = validated_data.pop('printer_specification_id', None)
#         extender_char_data = validated_data.pop('extender_char', None)
#         extender_specification = validated_data.pop('extender_specification_id', None)
#         router_char_data = validated_data.pop('router_char', None)
#         router_specification = validated_data.pop('router_specification_id', None)
#         tv_char_data = validated_data.pop('tv_char', None)
#         tv_specification = validated_data.pop('tv_specification_id', None)

#         # Получаем автора (оставлено без изменений)
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             validated_data['author'] = request.user

#         equipment = Equipment.objects.create(**validated_data)
#         type_name = equipment.type.name.lower()

#         # Логика для компьютеров (оставлена без изменений)
#         if type_name in self.COMPUTER_TYPES:
#             if computer_specification:
#                 spec = computer_specification
#                 if not isinstance(computer_specification, ComputerSpecification):
#                     spec = ComputerSpecification.objects.get(id=computer_specification)
#                 computer_details_data = {
#                     'cpu': spec.cpu,
#                     'ram': spec.ram,
#                     'storage': spec.storage,
#                     'has_keyboard': spec.has_keyboard,
#                     'has_mouse': spec.has_mouse,
#                     'monitor_size': spec.monitor_size,
#                 }
#             if computer_details_data:
#                 ComputerDetails.objects.create(equipment=equipment, **computer_details_data)

#         # Логика для принтеров
#         elif type_name in self.PRINTER_TYPES:
#             if printer_specification:
#                 spec = printer_specification
#                 if not isinstance(printer_specification, PrinterSpecification):
#                     spec = PrinterSpecification.objects.get(id=printer_specification)
#                 printer_char_data = {
#                     'model': spec.model,
#                     'color': spec.color,
#                     'duplex': spec.duplex,
#                     'author': request.user if request and request.user.is_authenticated else None,
#                 }
#             if printer_char_data:
#                 printer_char_data['serial_number'] = validated_data.get('inn', '')  # Или другой уникальный ID
#                 PrinterChar.objects.create(equipment=equipment, **printer_char_data)

#         # Логика для удлинителей
#         elif type_name in self.EXTENDER_TYPES:
#             if extender_specification:
#                 spec = extender_specification
#                 if not isinstance(extender_specification, ExtenderSpecification):
#                     spec = ExtenderSpecification.objects.get(id=extender_specification)
#                 extender_char_data = {
#                     'ports': spec.ports,
#                     'length': spec.length,
#                     'author': request.user if request and request.user.is_authenticated else None,
#                 }
#             if extender_char_data:
#                 ExtenderChar.objects.create(equipment=equipment, **extender_char_data)

#         # Логика для роутеров
#         elif type_name in self.ROUTER_TYPES:
#             if router_specification:
#                 spec = router_specification
#                 if not isinstance(router_specification, RouterSpecification):
#                     spec = RouterSpecification.objects.get(id=router_specification)
#                 router_char_data = {
#                     'model': spec.model,
#                     'ports': spec.ports,
#                     'wifi_standart': spec.wifi_standart,
#                     'author': request.user if request and request.user.is_authenticated else None,
#                 }
#             if router_char_data:
#                 router_char_data['serial_number'] = validated_data.get('inn', '')
#                 RouterChar.objects.create(equipment=equipment, **router_char_data)

#         # Логика для телевизоров
#         elif type_name in self.TV_TYPES:
#             if tv_specification:
#                 spec = tv_specification
#                 if not isinstance(tv_specification, TVSpecification):
#                     spec = TVSpecification.objects.get(id=tv_specification)
#                 tv_char_data = {
#                     'model': spec.model,
#                     'screen_size': spec.screen_size,
#                     'author': request.user if request and request.user.is_authenticated else None,
#                 }
#             if tv_char_data:
#                 tv_char_data['serial_number'] = validated_data.get('inn', '')
#                 TVChar.objects.create(equipment=equipment, **tv_char_data)

#         return equipment

#     def update(self, instance, validated_data):
#         # Существующие данные
#         computer_details_data = validated_data.pop('computer_details', None)
#         computer_specification_id = validated_data.pop('computer_specification_id', None)
#         # Новые данные
#         printer_char_data = validated_data.pop('printer_char', None)
#         printer_specification_id = validated_data.pop('printer_specification_id', None)
#         extender_char_data = validated_data.pop('extender_char', None)
#         extender_specification_id = validated_data.pop('extender_specification_id', None)
#         router_char_data = validated_data.pop('router_char', None)
#         router_specification_id = validated_data.pop('router_specification_id', None)
#         tv_char_data = validated_data.pop('tv_char', None)
#         tv_specification_id = validated_data.pop('tv_specification_id', None)
#         validated_data.pop('author', None)  # Запрещаем менять автора при обновлении

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         type_name = instance.type.name.lower()
#         request = self.context.get('request')

#         # Логика для компьютеров (оставлена без изменений)
#         if type_name in self.COMPUTER_TYPES:
#             if computer_specification_id:
#                 spec = ComputerSpecification.objects.get(id=computer_specification_id)
#                 computer_details_data = {
#                     'cpu': spec.cpu,
#                     'ram': spec.ram,
#                     'storage': spec.storage,
#                     'has_keyboard': spec.has_keyboard,
#                     'has_mouse': spec.has_mouse,
#                     'monitor_size': spec.monitor_size,
#                 }
#             if computer_details_data:
#                 try:
#                     computer_details = instance.computer_details
#                     for attr, value in computer_details_data.items():
#                         setattr(computer_details, attr, value)
#                     computer_details.save()
#                 except ComputerDetails.DoesNotExist:
#                     ComputerDetails.objects.create(equipment=instance, **computer_details_data)
#         elif hasattr(instance, 'computer_details'):
#             instance.computer_details.delete()

#         # Логика для принтеров
#         if type_name in self.PRINTER_TYPES:
#             if printer_specification_id:
#                 spec = PrinterSpecification.objects.get(id=printer_specification_id)
#                 printer_char_data = {
#                     'model': spec.model,
#                     'color': spec.color,
#                     'duplex': spec.duplex,
#                     'author': request.user if request and request.user.is_authenticated else None,
#                 }
#             if printer_char_data:
#                 try:
#                     printer_char = instance.printer_char
#                     for attr, value in printer_char_data.items():
#                         setattr(printer_char, attr, value)
#                     printer_char.serial_number = validated_data.get('inn', printer_char.serial_number)
#                     printer_char.author = request.user if request and request.user.is_authenticated else printer_char.author
#                     printer_char.save()
#                 except PrinterChar.DoesNotExist:
#                     printer_char_data['serial_number'] = validated_data.get('inn', '')
#                     PrinterChar.objects.create(equipment=instance, **printer_char_data)
#         elif hasattr(instance, 'printer_char'):
#             instance.printer_char.delete()

#         # Логика для удлинителей
#         if type_name in self.EXTENDER_TYPES:
#             if extender_specification_id:
#                 spec = ExtenderSpecification.objects.get(id=extender_specification_id)
#                 extender_char_data = {
#                     'ports': spec.ports,
#                     'length': spec.length,
#                     'author': request.user if request and request.user.is_authenticated else None,
#                 }
#             if extender_char_data:
#                 try:
#                     extender_char = instance.extender_char
#                     for attr, value in extender_char_data.items():
#                         setattr(extender_char, attr, value)
#                     extender_char.author = request.user if request and request.user.is_authenticated else extender_char.author
#                     extender_char.save()
#                 except ExtenderChar.DoesNotExist:
#                     ExtenderChar.objects.create(equipment=instance, **extender_char_data)
#         elif hasattr(instance, 'extender_char'):
#             instance.extender_char.delete()

#         # Логика для роутеров
#         if type_name in self.ROUTER_TYPES:
#             if router_specification_id:
#                 spec = RouterSpecification.objects.get(id=router_specification_id)
#                 router_char_data = {
#                     'model': spec.model,
#                     'ports': spec.ports,
#                     'wifi_standart': spec.wifi_standart,
#                     'author': request.user if request and request.user.is_authenticated else None,
#                 }
#             if router_char_data:
#                 try:
#                     router_char = instance.router_char
#                     for attr, value in router_char_data.items():
#                         setattr(router_char, attr, value)
#                     router_char.serial_number = validated_data.get('inn', router_char.serial_number)
#                     router_char.author = request.user if request and request.user.is_authenticated else router_char.author
#                     router_char.save()
#                 except RouterChar.DoesNotExist:
#                     router_char_data['serial_number'] = validated_data.get('inn', '')
#                     RouterChar.objects.create(equipment=instance, **router_char_data)
#         elif hasattr(instance, 'router_char'):
#             instance.router_char.delete()

#         # Логика для телевизоров
#         if type_name in self.TV_TYPES:
#             if tv_specification_id:
#                 spec = TVSpecification.objects.get(id=tv_specification_id)
#                 tv_char_data = {
#                     'model': spec.model,
#                     'screen_size': spec.screen_size,
#                     'author': request.user if request and request.user.is_authenticated else None,
#                 }
#             if tv_char_data:
#                 try:
#                     tv_char = instance.tv_char
#                     for attr, value in tv_char_data.items():
#                         setattr(tv_char, attr, value)
#                     tv_char.serial_number = validated_data.get('inn', tv_char.serial_number)
#                     tv_char.author = request.user if request and request.user.is_authenticated else tv_char.author
#                     tv_char.save()
#                 except TVChar.DoesNotExist:
#                     tv_char_data['serial_number'] = validated_data.get('inn', '')
#                     TVChar.objects.create(equipment=instance, **tv_char_data)
#         elif hasattr(instance, 'tv_char'):
#             instance.tv_char.delete()

#         return instance



# # class EquipmentSerializer(serializers.ModelSerializer):
# #     contract = ContractDocumentSerializer(read_only=True, allow_null=True)
# #     computer_details = ComputerDetailsSerializer(required=False, allow_null=True)
# #     computer_specification_id = serializers.PrimaryKeyRelatedField(
# #         queryset=ComputerSpecification.objects.all(),
# #         required=False,
# #         allow_null=True,
# #         write_only=True,
# #         help_text="ID шаблона компьютерной спецификации для автозаполнения характеристик"
# #     )
# #     PrinterChar = serializers.PrimaryKeyRelatedField(queryset=PrinterChar.objects.all(), required=False, allow_null=True)

# #     computer_specification_data = ComputerSpecificationSerializer(source='computer_details', read_only=True, allow_null=True)
# #     type = serializers.PrimaryKeyRelatedField(queryset=EquipmentType.objects.all())
# #     type_data = EquipmentTypeSerializer(source='type', read_only=True)
# #     room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), allow_null=True, required=False)
# #     room_data = RoomSerializer(source='room', read_only=True, allow_null=True)
# #     qr_code_url = serializers.SerializerMethodField()
# #     author = UserSerializer(read_only=True)
# #     author_id = serializers.PrimaryKeyRelatedField(
# #         queryset=User.objects.all(),
# #         write_only=True,
# #         required=False,
# #         allow_null=True,
# #         source='author'
# #     )

# #     class Meta:
# #         model = Equipment
# #         fields = [
# #             'id', 'type', 'type_data', 'room', 'room_data', 'name', 'photo', 'description',
# #             'is_active', 'contract', 'created_at', 'computer_details', 'computer_specification_id',
# #             'computer_specification_data', 'status', 'qr_code_url', 'uid', 'author', 'author_id', 'inn'
# #         ]
# #         read_only_fields = ['created_at', 'uid', 'author']

# #     def get_qr_code_url(self, obj):
# #         if obj.qr_code:
# #             return obj.qr_code.url
# #         return None

# #     def validate(self, data):
# #         equipment_type = data.get('type')
# #         computer_details = data.get('computer_details')
# #         computer_specification_id = data.get('computer_specification_id')

# #         is_computer = equipment_type and equipment_type.name.lower() in ('компьютер', 'ноутбук', 'моноблок')

# #         if is_computer and computer_details and computer_specification_id:
# #             raise serializers.ValidationError(
# #                 "Укажите либо computer_details, либо computer_specification_id, но не оба."
# #             )
# #         if not is_computer and (computer_details or computer_specification_id):
# #             raise serializers.ValidationError(
# #                 "Для этого типа оборудования компьютерные характеристики не поддерживаются."
# #             )

# #         return data

# #     def create(self, validated_data):
# #         computer_details_data = validated_data.pop('computer_details', None)
# #         computer_specification = validated_data.pop('computer_specification_id', None)

# #         # Получаем автора, если он передан или есть request
# #         request = self.context.get('request')
# #         if request and request.user.is_authenticated:
# #             validated_data['author'] = request.user

# #         equipment = Equipment.objects.create(**validated_data)

# #         if equipment.type.name.lower() in ('компьютер', 'ноутбук', 'моноблок'):
# #             if computer_specification:
# #                 spec = computer_specification
# #                 if not isinstance(computer_specification, ComputerSpecification):
# #                     spec = ComputerSpecification.objects.get(id=computer_specification)

# #                 computer_details_data = {
# #                     'cpu': spec.cpu,
# #                     'ram': spec.ram,
# #                     'storage': spec.storage,
# #                     'has_keyboard': spec.has_keyboard,
# #                     'has_mouse': spec.has_mouse,
# #                     'monitor_size': spec.monitor_size,
# #                 }

# #             if computer_details_data:
# #                 ComputerDetails.objects.create(equipment=equipment, **computer_details_data)

# #         return equipment


#     def update(self, instance, validated_data):
#         computer_details_data = validated_data.pop('computer_details', None)
#         computer_specification_id = validated_data.pop('computer_specification_id', None)
#         validated_data.pop('author', None)  # Запрещаем менять автора при обновлении

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         if instance.type.name.lower() == 'компьютер':
#             if computer_specification_id:
#                 spec = ComputerSpecification.objects.get(id=computer_specification_id)
#                 computer_details_data = {
#                     'cpu': spec.cpu,
#                     'ram': spec.ram,
#                     'storage': spec.storage,
#                     'has_keyboard': spec.has_keyboard,
#                     'has_mouse': spec.has_mouse,
#                     'monitor_size': spec.monitor_size,
#                 }
#             if computer_details_data:
#                 try:
#                     computer_details = instance.computer_details
#                     for attr, value in computer_details_data.items():
#                         setattr(computer_details, attr, value)
#                     computer_details.save()
#                 except ComputerDetails.DoesNotExist:
#                     ComputerDetails.objects.create(equipment=instance, **computer_details_data)
#         elif hasattr(instance, 'computer_details'):
#             instance.computer_details.delete()

#         return instance





# class MovementHistorySerializer(serializers.ModelSerializer):
#     equipment = serializers.StringRelatedField()
#     from_room = serializers.StringRelatedField()
#     to_room = serializers.StringRelatedField()

#     class Meta:
#         model = MovementHistory
#         fields = [
#             'id',
#             'equipment',
#             'from_room',
#             'to_room',
#             'moved_at',
#         ]


# class MoveEquipmentSerializer(serializers.Serializer):
#     equipment_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         min_length=1,
#         required=True
#     )
#     from_room_id = serializers.PrimaryKeyRelatedField(
#         queryset=Room.objects.all(),
#         required=True
#     )
#     to_room_id = serializers.PrimaryKeyRelatedField(
#         queryset=Room.objects.all(),
#         required=True
#     )

#     def validate(self, data):
#         equipment_ids = data['equipment_ids']
#         from_room = data['from_room_id']
#         to_room = data['to_room_id']

#         # Проверяем, что оборудование существует и принадлежит from_room
#         equipments = Equipment.objects.filter(id__in=equipment_ids, room=from_room)
#         if equipments.count() != len(equipment_ids):
#             raise serializers.ValidationError("Некоторые ID оборудования не найдены или не принадлежат указанному кабинету")

#         # Проверяем, что from_room и to_room не совпадают
#         if from_room == to_room:
#             raise serializers.ValidationError("Исходный и целевой кабинеты должны быть разными")

#         return data



# # Массовая генерация оборудовании

# class BulkEquipmentSerializer(serializers.Serializer):
#     type_id = serializers.PrimaryKeyRelatedField(
#         queryset=EquipmentType.objects.all(),
#         required=True
#     )
#     room_id = serializers.PrimaryKeyRelatedField(
#         queryset=Room.objects.all(),
#         required=False,
#         allow_null=True
#     )
#     description = serializers.CharField(required=False, allow_blank=True)
#     status = serializers.ChoiceField(
#         choices=Equipment.STATUS_CHOICES,
#         default='NEW'
#     )
#     contract_id = serializers.PrimaryKeyRelatedField(
#         queryset=ContractDocument.objects.all(),
#         required=False,
#         allow_null=True
#     )
#     count = serializers.IntegerField(min_value=1, max_value=100, required=True)
#     name_prefix = serializers.CharField(max_length=200, required=True)
#     computer_details = ComputerDetailsSerializer(required=False, allow_null=True)
#     computer_specification_id = serializers.PrimaryKeyRelatedField(
#         queryset=ComputerSpecification.objects.all(),
#         required=False,
#         allow_null=True
#     )
#     author_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         required=False,
#         allow_null=True
#     )

#     def validate(self, data):
#         equipment_type = data.get('type_id')
#         computer_details = data.get('computer_details')
#         computer_specification_id = data.get('computer_specification_id')

#         # Проверка типа оборудования
#         is_computer = equipment_type and equipment_type.name.lower() == 'компьютер'
#         if is_computer and computer_details and computer_specification_id:
#             raise serializers.ValidationError(
#                 "Укажите либо computer_details, либо computer_specification_id, но не оба."
#             )
#         if not is_computer and (computer_details or computer_specification_id):
#             raise serializers.ValidationError(
#                 "Для этого типа оборудования компьютерные характеристики не поддерживаются."
#             )

#         # Проверка существования комнаты
#         if data.get('room_id') and not Room.objects.filter(id=data['room_id'].id).exists():
#             raise serializers.ValidationError({"room_id": "Кабинет не найден"})

#         return data

#     def create(self, validated_data):
#         count = validated_data.pop('count')
#         name_prefix = validated_data.pop('name_prefix')
#         computer_details_data = validated_data.pop('computer_details', None)
#         computer_specification = validated_data.pop('computer_specification_id', None)
#         author = validated_data.pop('author_id', None)
#         request = self.context.get('request')

#         # Устанавливаем автора
#         if not author and request and request.user.is_authenticated:
#             author = request.user

#         equipments = []

#         # Получаем данные спецификации, если указана
#         if computer_specification:
#             spec = computer_specification
#             computer_details_data = {
#                 'cpu': spec.cpu,
#                 'ram': spec.ram,
#                 'storage': spec.storage,
#                 'has_keyboard': spec.has_keyboard,
#                 'has_mouse': spec.has_mouse,
#                 'monitor_size': spec.monitor_size,
#             }

#         for i in range(count):
#             equipment_data = {
#                 'type': validated_data['type_id'],
#                 'room': validated_data.get('room_id'),
#                 'name': f"{name_prefix} {i + 1}",
#                 'description': validated_data.get('description', ''),
#                 'status': validated_data['status'],
#                 'contract': validated_data.get('contract_id'),
#                 'author': author,
#                 'inn': 0,  # ИНН будет задан на втором этапе
#                 'is_active': True
#             }

#             equipment = Equipment.objects.create(**equipment_data)

#             if equipment.type.name.lower() == 'компьютер' and computer_details_data:
#                 ComputerDetails.objects.create(equipment=equipment, **computer_details_data)

#             equipments.append(equipment)

#         return equipments

# class BulkEquipmentInnUpdateSerializer(serializers.Serializer):
#     equipments = serializers.ListField(
#         child=serializers.DictField(
#             child=serializers.IntegerField(),
#             required=True
#         ),
#         min_length=1
#     )

#     def validate(self, data):
#         equipment_data = data['equipments']
#         equipment_ids = [item['id'] for item in equipment_data]
#         inns = [item['inn'] for item in equipment_data]

#         # Проверяем, что все ID существуют
#         existing_equipments = Equipment.objects.filter(id__in=equipment_ids)
#         if existing_equipments.count() != len(equipment_ids):
#             raise serializers.ValidationError("Некоторые ID оборудования не найдены")

#         # Проверяем, что все оборудования принадлежат текущему пользователю
#         user = self.context['request'].user
#         if existing_equipments.filter(author=user).count() != len(equipment_ids):
#             raise serializers.ValidationError("Вы можете обновлять только своё оборудование")

#         # Проверяем уникальность ИНН
#         if len(inns) != len(set(inns)):
#             raise serializers.ValidationError("ИНН должны быть уникальными")

#         return data

#     def update(self, validated_data):
#         equipment_data = validated_data['equipments']
#         equipments = []

#         for item in equipment_data:
#             equipment = Equipment.objects.get(id=item['id'])
#             equipment.inn = item['inn']
#             equipment.save()
#             equipments.append(equipment)

#         return equipments


from rest_framework import serializers
from .models import (EquipmentType, Equipment, ComputerDetails,
                     MovementHistory, ContractDocument, ComputerSpecification,
                     RouterSpecification, ExtenderSpecification, TVSpecification, PrinterSpecification,
                     RouterChar, ExtenderChar, TVChar, PrinterChar,
                     NotebookChar, NotebookSpecification, MonoblokChar, MonoblokSpecification,
                     ProjectorChar, ProjectorSpecification, WhiteboardChar, WhiteboardSpecification)
from university.models import Room
from university.serializers import RoomSerializer
from user.serializers import UserSerializer

from io import BytesIO
import qrcode
from django.core.files import File
from django.contrib.auth import get_user_model

User = get_user_model()

class EquipmentTypeSerializer(serializers.ModelSerializer):
    requires_computer_details = serializers.SerializerMethodField()

    def get_requires_computer_details(self, obj):
        # Считаем, что только тип с name="Компьютер" требует характеристики
        computer_types = ['компьютер', 'ноутбук', 'моноблок']
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


class ComputerSpecificationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='author'
    )
    class Meta:
        model = ComputerSpecification
        fields = [
            'id', 'cpu', 'ram', 'storage', 'has_keyboard', 'has_mouse',
            'monitor_size', 'created_at', 'uid', 'author', 'author_id'
        ]
        read_only_fields = ['created_at', 'uid', 'author', 'author_id']



class PrinterCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterChar
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')


class ExtenderCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtenderChar
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')


class RouterCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterChar
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')


class TVCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVChar
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')


class PrinterSpecificationSerializer(serializers.ModelSerializer):
    def get_queryset(self):
        user = self.context['request'].user
        if user.is_authenticated:
            return PrinterSpecification.objects.filter(author=user)
        return PrinterSpecification.objects.none()

    class Meta:
        model = PrinterSpecification
        fields = ['id', 'model', 'color', 'duplex', 'author', 'created_at', 'updated_at']

class ExtenderSpecificationSerializer(serializers.ModelSerializer):
    length = serializers.FloatField()

    def get_queryset(self):
        user = self.context['request'].user
        if user.is_authenticated:
            return ExtenderSpecification.objects.filter(author=user)
        return ExtenderSpecification.objects.none()

    class Meta:
        model = ExtenderSpecification
        fields = ['id', 'ports', 'length', 'author', 'created_at', 'updated_at']

class RouterSpecificationSerializer(serializers.ModelSerializer):
    WIFI_STANDARDS = [
        ('802.11n', 'Wi-Fi 4'),
        ('802.11ac', 'Wi-Fi 5'),
        ('802.11ax', 'Wi-Fi 6'),
    ]
    wifi_standart = serializers.ChoiceField(choices=WIFI_STANDARDS)

    def get_queryset(self):
        user = self.context['request'].user
        if user.is_authenticated:
            return RouterSpecification.objects.filter(author=user)
        return RouterSpecification.objects.none()

    class Meta:
        model = RouterSpecification
        fields = ['id', 'model', 'ports', 'wifi_standart', 'author', 'created_at', 'updated_at']

class TVSpecificationSerializer(serializers.ModelSerializer):
    screen_size = serializers.IntegerField()

    def get_queryset(self):
        user = self.context['request'].user
        if user.is_authenticated:
            return TVSpecification.objects.filter(author=user)
        return TVSpecification.objects.none()

    class Meta:
        model = TVSpecification
        fields = ['id', 'model', 'screen_size', 'author', 'created_at', 'updated_at']



#############################################
class NotebookCharSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = NotebookChar
        fields = ['id', 'cpu', 'ram', 'storage', 'monitor_size', 'author', 'created_at', 'updated_at']

class NotebookSpecificationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    def get_queryset(self):
        user = self.context['request'].user
        if user.is_authenticated:
            return NotebookSpecification.objects.filter(author=user)
        return NotebookSpecification.objects.none()

    class Meta:
        model = NotebookSpecification
        fields = ['id', 'cpu', 'ram', 'storage', 'monitor_size', 'author', 'created_at', 'updated_at']

class MonoblokCharSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = MonoblokChar
        fields = ['id', 'cpu', 'ram', 'storage', 'has_keyboard', 'has_mouse', 'monitor_size', 'author', 'created_at', 'updated_at']

class MonoblokSpecificationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    def get_queryset(self):
        user = self.context['request'].user
        if user.is_authenticated:
            return MonoblokSpecification.objects.filter(author=user)
        return MonoblokSpecification.objects.none()

    class Meta:
        model = MonoblokSpecification
        fields = ['id', 'cpu', 'ram', 'storage', 'has_keyboard', 'has_mouse', 'monitor_size', 'author', 'created_at', 'updated_at']


class ProjectorCharSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = ProjectorChar
        fields = ['id', 'model', 'lumens', 'resolution', 'throw_type', 'author', 'created_at', 'updated_at']

class ProjectorSpecificationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = ProjectorSpecification
        fields = ['id', 'model', 'lumens', 'resolution', 'throw_type', 'author', 'created_at', 'updated_at']

class WhiteboardCharSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = WhiteboardChar
        fields = ['id', 'model', 'screen_size', 'touch_type',  'author', 'created_at', 'updated_at']

class WhiteboardSpecificationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = WhiteboardSpecification
        fields = ['id', 'model', 'screen_size', 'touch_type', 'author', 'created_at', 'updated_at']


#######################################################

import re
class EquipmentFromLinkSerializer(serializers.Serializer):
    room_link = serializers.URLField(required=True)

    def validate_room_link(self, value):
        match = re.match(r'.*/rooms/(\d+)/\?building=(\d+)', value)
        if not match:
            raise serializers.ValidationError("Неверный формат ссылки")
        room_id, building_id = match.groups()
        try:
            room = Room.objects.get(id=room_id, building_id=building_id)
        except Room.DoesNotExist:
            raise serializers.ValidationError("Кабинет или корпус не найдены")
        return {'room_id': room_id, 'building_id': building_id, 'room': room}

class EquipmentSerializer(serializers.ModelSerializer):
    COMPUTER_TYPES = {'компьютер', 'ноутбук', 'моноблок'}
    PRINTER_TYPES = {'принтер', 'мфу'}
    EXTENDER_TYPES = {'удлинитель', 'сетевой фильтр'}
    ROUTER_TYPES = {'роутер'}
    TV_TYPES = {'телевизор'}
    PROJECTOR_TYPES = {'проектор'}
    WHITEBOARD_TYPES = {'электронная доска'}

    # Существующие поля
    contract = ContractDocumentSerializer(read_only=True, allow_null=True)
    type = serializers.PrimaryKeyRelatedField(queryset=EquipmentType.objects.all())
    type_data = EquipmentTypeSerializer(source='type', read_only=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), allow_null=True, required=False)
    room_data = RoomSerializer(source='room', read_only=True, allow_null=True)
    qr_code_url = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='author'
    )

    # Поля для характеристик
    computer_details = ComputerDetailsSerializer(required=False, allow_null=True)
    printer_char = PrinterCharSerializer(required=False, allow_null=True)
    extender_char = ExtenderCharSerializer(required=False, allow_null=True)
    router_char = RouterCharSerializer(required=False, allow_null=True)
    tv_char = TVCharSerializer(required=False, allow_null=True)
    notebook_char = NotebookCharSerializer(required=False, allow_null=True)
    monoblok_char = MonoblokCharSerializer(required=False, allow_null=True)
    projector_char = ProjectorCharSerializer(required=False, allow_null=True)
    whiteboard_char = WhiteboardCharSerializer(required=False, allow_null=True)

    # Поля для шаблонов
    computer_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=ComputerSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона компьютерной спецификации для автозаполнения характеристик"
    )
    printer_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=PrinterSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона спецификации принтера для автозаполнения характеристик"
    )
    extender_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=ExtenderSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона спецификации удлинителя для автозаполнения характеристик"
    )
    router_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=RouterSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона спецификации роутера для автозаполнения характеристик"
    )
    tv_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=TVSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона спецификации телевизора для автозаполнения характеристик"
    )
    notebook_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=NotebookSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона спецификации ноутбука для автозаполнения характеристик"
    )
    monoblok_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=MonoblokSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона спецификации моноблока для автозаполнения характеристик"
    )
    projector_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectorSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона спецификации проектора для автозаполнения характеристик"
    )
    whiteboard_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=WhiteboardSpecification.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        help_text="ID шаблона спецификации электронной доски для автозаполнения характеристик"
    )

    # Поля для отображения данных спецификаций
    computer_specification_data = ComputerSpecificationSerializer(source='computer_details', read_only=True, allow_null=True)
    printer_specification_data = PrinterSpecificationSerializer(source='printer_char', read_only=True, allow_null=True)
    extender_specification_data = ExtenderSpecificationSerializer(source='extender_char', read_only=True, allow_null=True)
    router_specification_data = RouterSpecificationSerializer(source='router_char', read_only=True, allow_null=True)
    tv_specification_data = TVSpecificationSerializer(source='tv_char', read_only=True, allow_null=True)
    notebook_specification_data = NotebookSpecificationSerializer(source='notebook_char', read_only=True, allow_null=True)
    monoblok_specification_data = MonoblokSpecificationSerializer(source='monoblok_char', read_only=True, allow_null=True)
    projector_specification_data = ProjectorSpecificationSerializer(source='projector_char', read_only=True, allow_null=True)
    whiteboard_specification_data = WhiteboardSpecificationSerializer(source='whiteboard_char', read_only=True, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Фильтрация шаблонов по автору
            self.fields['computer_specification_id'].queryset = ComputerSpecification.objects.filter(author=request.user)
            self.fields['printer_specification_id'].queryset = PrinterSpecification.objects.filter(author=request.user)
            self.fields['extender_specification_id'].queryset = ExtenderSpecification.objects.filter(author=request.user)
            self.fields['router_specification_id'].queryset = RouterSpecification.objects.filter(author=request.user)
            self.fields['tv_specification_id'].queryset = TVSpecification.objects.filter(author=request.user)
            self.fields['notebook_specification_id'].queryset = NotebookSpecification.objects.filter(author=request.user)
            self.fields['monoblok_specification_id'].queryset = MonoblokSpecification.objects.filter(author=request.user)
            self.fields['projector_specification_id'].queryset = ProjectorSpecification.objects.filter(author=request.user)
            self.fields['whiteboard_specification_id'].queryset = WhiteboardSpecification.objects.filter(author=request.user)
        else:
            # Для анонимных пользователей — пустой queryset
            for field in [
                'computer_specification_id', 'printer_specification_id', 'extender_specification_id',
                'router_specification_id', 'tv_specification_id', 'notebook_specification_id',
                'monoblok_specification_id', 'projector_specification_id', 'whiteboard_specification_id'
            ]:
                self.fields[field].queryset = self.fields[field].queryset.none()

    class Meta:
        model = Equipment
        fields = [
            'id', 'type', 'type_data', 'room', 'room_data', 'name', 'photo', 'description',
            'is_active', 'contract', 'created_at', 'computer_details', 'computer_specification_id',
            'computer_specification_data', 'printer_char', 'printer_specification_id',
            'printer_specification_data', 'extender_char', 'extender_specification_id',
            'extender_specification_data', 'router_char', 'router_specification_id',
            'router_specification_data', 'tv_char', 'tv_specification_id',
            'tv_specification_data', 'notebook_char', 'notebook_specification_id',
            'notebook_specification_data', 'monoblok_char', 'monoblok_specification_id',
            'monoblok_specification_data', 'projector_char', 'projector_specification_id',
            'projector_specification_data', 'whiteboard_char', 'whiteboard_specification_id',
            'whiteboard_specification_data', 'status', 'qr_code_url', 'uid', 'author', 'author_id', 'inn'
        ]
        read_only_fields = ['created_at', 'uid', 'author']

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None

    def validate(self, data):
        equipment_type = data.get('type')
        if not equipment_type:
            raise serializers.ValidationError("Поле type обязательно.")

        type_name = equipment_type.name.lower()
        computer_details = data.get('computer_details')
        computer_specification_id = data.get('computer_specification_id')
        printer_char = data.get('printer_char')
        printer_specification_id = data.get('printer_specification_id')
        extender_char = data.get('extender_char')
        extender_specification_id = data.get('extender_specification_id')
        router_char = data.get('router_char')
        router_specification_id = data.get('router_specification_id')
        tv_char = data.get('tv_char')
        tv_specification_id = data.get('tv_specification_id')
        notebook_char = data.get('notebook_char')
        notebook_specification_id = data.get('notebook_specification_id')
        monoblok_char = data.get('monoblok_char')
        monoblok_specification_id = data.get('monoblok_specification_id')
        projector_char = data.get('projector_char')
        projector_specification_id = data.get('projector_specification_id')
        whiteboard_char = data.get('whiteboard_char')
        whiteboard_specification_id = data.get('whiteboard_specification_id')

        # Проверка для компьютеров
        is_computer = type_name in self.COMPUTER_TYPES
        if is_computer:
            provided_specs = sum(bool(x) for x in [
                computer_details, computer_specification_id,
                notebook_char, notebook_specification_id,
                monoblok_char, monoblok_specification_id
            ])
            if provided_specs > 1:
                raise serializers.ValidationError(
                    "Укажите только один тип характеристик или шаблон для компьютеров (computer_details, notebook_char, monoblok_char или их шаблоны)."
                )
            if provided_specs == 0:
                raise serializers.ValidationError(
                    "Для компьютеров требуется указать computer_details, notebook_char, monoblok_char или их шаблоны."
                )
        elif computer_details or computer_specification_id or notebook_char or notebook_specification_id or monoblok_char or monoblok_specification_id:
            raise serializers.ValidationError(
                "Характеристики компьютеров поддерживаются только для типов 'компьютер', 'ноутбук', 'моноблок'."
            )

        # Проверка для принтеров
        is_printer = type_name in self.PRINTER_TYPES
        if is_printer:
            if printer_char and printer_specification_id:
                raise serializers.ValidationError(
                    "Укажите либо printer_char, либо printer_specification_id, но не оба."
                )
            if not printer_char and not printer_specification_id:
                raise serializers.ValidationError(
                    "Для принтеров требуется указать printer_char или printer_specification_id."
                )
        elif printer_char or printer_specification_id:
            raise serializers.ValidationError(
                "Характеристики принтеров поддерживаются только для принтеров."
            )

        # Проверка для удлинителей
        is_extender = type_name in self.EXTENDER_TYPES
        if is_extender:
            if extender_char and extender_specification_id:
                raise serializers.ValidationError(
                    "Укажите либо extender_char, либо extender_specification_id, но не оба."
                )
            if not extender_char and not extender_specification_id:
                raise serializers.ValidationError(
                    "Для удлинителей требуется указать extender_char или extender_specification_id."
                )
        elif extender_char or extender_specification_id:
            raise serializers.ValidationError(
                "Характеристики удлинителей поддерживаются только для удлинителей."
            )

        # Проверка для роутеров
        is_router = type_name in self.ROUTER_TYPES
        if is_router:
            if router_char and router_specification_id:
                raise serializers.ValidationError(
                    "Укажите либо router_char, либо router_specification_id, но не оба."
                )
            if not router_char and not router_specification_id:
                raise serializers.ValidationError(
                    "Для роутеров требуется указать router_char или router_specification_id."
                )
        elif router_char or router_specification_id:
            raise serializers.ValidationError(
                "Характеристики роутеров поддерживаются только для роутеров."
            )

        # Проверка для телевизоров
        is_tv = type_name in self.TV_TYPES
        if is_tv:
            if tv_char and tv_specification_id:
                raise serializers.ValidationError(
                    "Укажите либо tv_char, либо tv_specification_id, но не оба."
                )
            if not tv_char and not tv_specification_id:
                raise serializers.ValidationError(
                    "Для телевизоров требуется указать tv_char или tv_specification_id."
                )
        elif tv_char or tv_specification_id:
            raise serializers.ValidationError(
                "Характеристики телевизоров поддерживаются только для телевизоров."
            )

        # Проверка для проекторов
        is_projector = type_name in self.PROJECTOR_TYPES
        if is_projector:
            if projector_char and projector_specification_id:
                raise serializers.ValidationError(
                    "Укажите либо projector_char, либо projector_specification_id, но не оба."
                )
            if not projector_char and not projector_specification_id:
                raise serializers.ValidationError(
                    "Для проекторов требуется указать projector_char или projector_specification_id."
                )
        elif projector_char or projector_specification_id:
            raise serializers.ValidationError(
                "Характеристики проекторов поддерживаются только для проекторов."
            )

        # Проверка для электронных досок
        is_whiteboard = type_name in self.WHITEBOARD_TYPES
        if is_whiteboard:
            if whiteboard_char and whiteboard_specification_id:
                raise serializers.ValidationError(
                    "Укажите либо whiteboard_char, либо whiteboard_specification_id, но не оба."
                )
            if not whiteboard_char and not whiteboard_specification_id:
                raise serializers.ValidationError(
                    "Для электронных досок требуется указать whiteboard_char или whiteboard_specification_id."
                )
        elif whiteboard_char or whiteboard_specification_id:
            raise serializers.ValidationError(
                "Характеристики электронных досок поддерживаются только для электронных досок."
            )

        return data

    def create(self, validated_data):
        # Извлечение данных характеристик и шаблонов
        computer_details_data = validated_data.pop('computer_details', None)
        computer_specification = validated_data.pop('computer_specification_id', None)
        printer_char_data = validated_data.pop('printer_char', None)
        printer_specification = validated_data.pop('printer_specification_id', None)
        extender_char_data = validated_data.pop('extender_char', None)
        extender_specification = validated_data.pop('extender_specification_id', None)
        router_char_data = validated_data.pop('router_char', None)
        router_specification = validated_data.pop('router_specification_id', None)
        tv_char_data = validated_data.pop('tv_char', None)
        tv_specification = validated_data.pop('tv_specification_id', None)
        notebook_char_data = validated_data.pop('notebook_char', None)
        notebook_specification = validated_data.pop('notebook_specification_id', None)
        monoblok_char_data = validated_data.pop('monoblok_char', None)
        monoblok_specification = validated_data.pop('monoblok_specification_id', None)
        projector_char_data = validated_data.pop('projector_char', None)
        projector_specification = validated_data.pop('projector_specification_id', None)
        whiteboard_char_data = validated_data.pop('whiteboard_char', None)
        whiteboard_specification = validated_data.pop('whiteboard_specification_id', None)

        # Получение автора
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user

        equipment = Equipment.objects.create(**validated_data)
        type_name = equipment.type.name.lower()

        # Логика для компьютеров
        if type_name in self.COMPUTER_TYPES:
            if computer_specification:
                spec = computer_specification
                if not isinstance(computer_specification, ComputerSpecification):
                    spec = ComputerSpecification.objects.get(id=computer_specification)
                computer_details_data = {
                    'cpu': spec.cpu,
                    'ram': spec.ram,
                    'storage': spec.storage,
                    'has_keyboard': spec.has_keyboard,
                    'has_mouse': spec.has_mouse,
                    'monitor_size': spec.monitor_size,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if computer_details_data:
                ComputerDetails.objects.create(equipment=equipment, **computer_details_data)

            if notebook_specification:
                spec = notebook_specification
                if not isinstance(notebook_specification, NotebookSpecification):
                    spec = NotebookSpecification.objects.get(id=notebook_specification)
                notebook_char_data = {
                    'cpu': spec.cpu,
                    'ram': spec.ram,
                    'storage': spec.storage,
                    'monitor_size': spec.monitor_size,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if notebook_char_data:
                NotebookChar.objects.create(equipment=equipment, **notebook_char_data)

            if monoblok_specification:
                spec = monoblok_specification
                if not isinstance(monoblok_specification, MonoblokSpecification):
                    spec = MonoblokSpecification.objects.get(id=monoblok_specification)
                monoblok_char_data = {
                    'cpu': spec.cpu,
                    'ram': spec.ram,
                    'storage': spec.storage,
                    'has_keyboard': spec.has_keyboard,
                    'has_mouse': spec.has_mouse,
                    'monitor_size': spec.monitor_size,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if monoblok_char_data:
                MonoblokChar.objects.create(equipment=equipment, **monoblok_char_data)

        # Логика для принтеров
        elif type_name in self.PRINTER_TYPES:
            if printer_specification:
                spec = printer_specification
                if not isinstance(printer_specification, PrinterSpecification):
                    spec = PrinterSpecification.objects.get(id=printer_specification)
                printer_char_data = {
                    'model': spec.model,
                    'color': spec.color,
                    'duplex': spec.duplex,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if printer_char_data:
                printer_char_data['serial_number'] = validated_data.get('inn', '')
                PrinterChar.objects.create(equipment=equipment, **printer_char_data)

        # Логика для удлинителей
        elif type_name in self.EXTENDER_TYPES:
            if extender_specification:
                spec = extender_specification
                if not isinstance(extender_specification, ExtenderSpecification):
                    spec = ExtenderSpecification.objects.get(id=extender_specification)
                extender_char_data = {
                    'ports': spec.ports,
                    'length': spec.length,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if extender_char_data:
                ExtenderChar.objects.create(equipment=equipment, **extender_char_data)

        # Логика для роутеров
        elif type_name in self.ROUTER_TYPES:
            if router_specification:
                spec = router_specification
                if not isinstance(router_specification, RouterSpecification):
                    spec = RouterSpecification.objects.get(id=router_specification)
                router_char_data = {
                    'model': spec.model,
                    'ports': spec.ports,
                    'wifi_standart': spec.wifi_standart,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if router_char_data:
                router_char_data['serial_number'] = validated_data.get('inn', '')
                RouterChar.objects.create(equipment=equipment, **router_char_data)

        # Логика для телевизоров
        elif type_name in self.TV_TYPES:
            if tv_specification:
                spec = tv_specification
                if not isinstance(tv_specification, TVSpecification):
                    spec = TVSpecification.objects.get(id=tv_specification)
                tv_char_data = {
                    'model': spec.model,
                    'screen_size': spec.screen_size,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if tv_char_data:
                tv_char_data['serial_number'] = validated_data.get('inn', '')
                TVChar.objects.create(equipment=equipment, **tv_char_data)

        # Логика для проекторов
        elif type_name in self.PROJECTOR_TYPES:
            if projector_specification:
                spec = projector_specification
                if not isinstance(projector_specification, ProjectorSpecification):
                    spec = ProjectorSpecification.objects.get(id=projector_specification)
                projector_char_data = {
                    'model': spec.model,
                    'lumens': spec.lumens,
                    'resolution': spec.resolution,
                    'throw_type': spec.throw_type,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if projector_char_data:
                ProjectorChar.objects.create(equipment=equipment, **projector_char_data)

        # Логика для электронных досок
        elif type_name in self.WHITEBOARD_TYPES:
            if whiteboard_specification:
                spec = whiteboard_specification
                if not isinstance(whiteboard_specification, WhiteboardSpecification):
                    spec = WhiteboardSpecification.objects.get(id=whiteboard_specification)
                whiteboard_char_data = {
                    'model': spec.model,
                    'screen_size': spec.screen_size,
                    'touch_type': spec.touch_type,
                    'touch_points': spec.touch_points,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if whiteboard_char_data:
                WhiteboardChar.objects.create(equipment=equipment, **whiteboard_char_data)

        return equipment

    def update(self, instance, validated_data):
        # Извлечение данных характеристик и шаблонов
        computer_details_data = validated_data.pop('computer_details', None)
        computer_specification_id = validated_data.pop('computer_specification_id', None)
        printer_char_data = validated_data.pop('printer_char', None)
        printer_specification_id = validated_data.pop('printer_specification_id', None)
        extender_char_data = validated_data.pop('extender_char', None)
        extender_specification_id = validated_data.pop('extender_specification_id', None)
        router_char_data = validated_data.pop('router_char', None)
        router_specification_id = validated_data.pop('router_specification_id', None)
        tv_char_data = validated_data.pop('tv_char', None)
        tv_specification_id = validated_data.pop('tv_specification_id', None)
        notebook_char_data = validated_data.pop('notebook_char', None)
        notebook_specification_id = validated_data.pop('notebook_specification_id', None)
        monoblok_char_data = validated_data.pop('monoblok_char', None)
        monoblok_specification_id = validated_data.pop('monoblok_specification_id', None)
        projector_char_data = validated_data.pop('projector_char', None)
        projector_specification_id = validated_data.pop('projector_specification_id', None)
        whiteboard_char_data = validated_data.pop('whiteboard_char', None)
        whiteboard_specification_id = validated_data.pop('whiteboard_specification_id', None)
        validated_data.pop('author', None)  # Запрещаем менять автора при обновлении

        # Обновление основных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        type_name = instance.type.name.lower()
        request = self.context.get('request')

        # Логика для компьютеров
        if type_name in self.COMPUTER_TYPES:
            if computer_specification_id:
                spec = ComputerSpecification.objects.get(id=computer_specification_id)
                computer_details_data = {
                    'cpu': spec.cpu,
                    'ram': spec.ram,
                    'storage': spec.storage,
                    'has_keyboard': spec.has_keyboard,
                    'has_mouse': spec.has_mouse,
                    'monitor_size': spec.monitor_size,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if computer_details_data:
                try:
                    computer_details = instance.computer_details
                    for attr, value in computer_details_data.items():
                        setattr(computer_details, attr, value)
                    computer_details.author = request.user if request and request.user.is_authenticated else computer_details.author
                    computer_details.save()
                except ComputerDetails.DoesNotExist:
                    ComputerDetails.objects.create(equipment=instance, **computer_details_data)
            elif hasattr(instance, 'computer_details'):
                instance.computer_details.delete()

            if notebook_specification_id:
                spec = NotebookSpecification.objects.get(id=notebook_specification_id)
                notebook_char_data = {
                    'cpu': spec.cpu,
                    'ram': spec.ram,
                    'storage': spec.storage,
                    'monitor_size': spec.monitor_size,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if notebook_char_data:
                try:
                    notebook_char = instance.notebook_char
                    for attr, value in notebook_char_data.items():
                        setattr(notebook_char, attr, value)
                    notebook_char.author = request.user if request and request.user.is_authenticated else notebook_char.author
                    notebook_char.save()
                except NotebookChar.DoesNotExist:
                    NotebookChar.objects.create(equipment=instance, **notebook_char_data)
            elif hasattr(instance, 'notebook_char'):
                instance.notebook_char.delete()

            if monoblok_specification_id:
                spec = MonoblokSpecification.objects.get(id=monoblok_specification_id)
                monoblok_char_data = {
                    'cpu': spec.cpu,
                    'ram': spec.ram,
                    'storage': spec.storage,
                    'has_keyboard': spec.has_keyboard,
                    'has_mouse': spec.has_mouse,
                    'monitor_size': spec.monitor_size,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if monoblok_char_data:
                try:
                    monoblok_char = instance.monoblok_char
                    for attr, value in monoblok_char_data.items():
                        setattr(monoblok_char, attr, value)
                    monoblok_char.author = request.user if request and request.user.is_authenticated else monoblok_char.author
                    monoblok_char.save()
                except MonoblokChar.DoesNotExist:
                    MonoblokChar.objects.create(equipment=instance, **monoblok_char_data)
            elif hasattr(instance, 'monoblok_char'):
                instance.monoblok_char.delete()

        # Логика для принтеров
        elif type_name in self.PRINTER_TYPES:
            if printer_specification_id:
                spec = PrinterSpecification.objects.get(id=printer_specification_id)
                printer_char_data = {
                    'model': spec.model,
                    'color': spec.color,
                    'duplex': spec.duplex,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if printer_char_data:
                try:
                    printer_char = instance.printer_char
                    for attr, value in printer_char_data.items():
                        setattr(printer_char, attr, value)
                    printer_char.serial_number = validated_data.get('inn', printer_char.serial_number)
                    printer_char.author = request.user if request and request.user.is_authenticated else printer_char.author
                    printer_char.save()
                except PrinterChar.DoesNotExist:
                    printer_char_data['serial_number'] = validated_data.get('inn', '')
                    PrinterChar.objects.create(equipment=instance, **printer_char_data)
        elif hasattr(instance, 'printer_char'):
            instance.printer_char.delete()

        # Логика для удлинителей
        elif type_name in self.EXTENDER_TYPES:
            if extender_specification_id:
                spec = ExtenderSpecification.objects.get(id=extender_specification_id)
                extender_char_data = {
                    'ports': spec.ports,
                    'length': spec.length,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if extender_char_data:
                try:
                    extender_char = instance.extender_char
                    for attr, value in extender_char_data.items():
                        setattr(extender_char, attr, value)
                    extender_char.author = request.user if request and request.user.is_authenticated else extender_char.author
                    extender_char.save()
                except ExtenderChar.DoesNotExist:
                    ExtenderChar.objects.create(equipment=instance, **extender_char_data)
        elif hasattr(instance, 'extender_char'):
            instance.extender_char.delete()

        # Логика для роутеров
        elif type_name in self.ROUTER_TYPES:
            if router_specification_id:
                spec = RouterSpecification.objects.get(id=router_specification_id)
                router_char_data = {
                    'model': spec.model,
                    'ports': spec.ports,
                    'wifi_standart': spec.wifi_standart,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if router_char_data:
                try:
                    router_char = instance.router_char
                    for attr, value in router_char_data.items():
                        setattr(router_char, attr, value)
                    router_char.serial_number = validated_data.get('inn', router_char.serial_number)
                    router_char.author = request.user if request and request.user.is_authenticated else router_char.author
                    router_char.save()
                except RouterChar.DoesNotExist:
                    router_char_data['serial_number'] = validated_data.get('inn', '')
                    RouterChar.objects.create(equipment=instance, **router_char_data)
        elif hasattr(instance, 'router_char'):
            instance.router_char.delete()

        # Логика для телевизоров
        elif type_name in self.TV_TYPES:
            if tv_specification_id:
                spec = TVSpecification.objects.get(id=tv_specification_id)
                tv_char_data = {
                    'model': spec.model,
                    'screen_size': spec.screen_size,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if tv_char_data:
                try:
                    tv_char = instance.tv_char
                    for attr, value in tv_char_data.items():
                        setattr(tv_char, attr, value)
                    tv_char.serial_number = validated_data.get('inn', tv_char.serial_number)
                    tv_char.author = request.user if request and request.user.is_authenticated else tv_char.author
                    tv_char.save()
                except TVChar.DoesNotExist:
                    tv_char_data['serial_number'] = validated_data.get('inn', '')
                    TVChar.objects.create(equipment=instance, **tv_char_data)
        elif hasattr(instance, 'tv_char'):
            instance.tv_char.delete()

        # Логика для проекторов
        elif type_name in self.PROJECTOR_TYPES:
            if projector_specification_id:
                spec = ProjectorSpecification.objects.get(id=projector_specification_id)
                projector_char_data = {
                    'model': spec.model,
                    'lumens': spec.lumens,
                    'resolution': spec.resolution,
                    'throw_type': spec.throw_type,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if projector_char_data:
                try:
                    projector_char = instance.projector_char
                    for attr, value in projector_char_data.items():
                        setattr(projector_char, attr, value)
                    projector_char.author = request.user if request and request.user.is_authenticated else projector_char.author
                    projector_char.save()
                except ProjectorChar.DoesNotExist:
                    ProjectorChar.objects.create(equipment=instance, **projector_char_data)
        elif hasattr(instance, 'projector_char'):
            instance.projector_char.delete()

        # Логика для электронных досок
        elif type_name in self.WHITEBOARD_TYPES:
            if whiteboard_specification_id:
                spec = WhiteboardSpecification.objects.get(id=whiteboard_specification_id)
                whiteboard_char_data = {
                    'model': spec.model,
                    'screen_size': spec.screen_size,
                    'touch_type': spec.touch_type,
                    'touch_points': spec.touch_points,
                    'author': request.user if request and request.user.is_authenticated else None,
                }
            if whiteboard_char_data:
                try:
                    whiteboard_char = instance.whiteboard_char
                    for attr, value in whiteboard_char_data.items():
                        setattr(whiteboard_char, attr, value)
                    whiteboard_char.author = request.user if request and request.user.is_authenticated else whiteboard_char.author
                    whiteboard_char.save()
                except WhiteboardChar.DoesNotExist:
                    WhiteboardChar.objects.create(equipment=instance, **whiteboard_char_data)
        elif hasattr(instance, 'whiteboard_char'):
            instance.whiteboard_char.delete()

        return instance

# class EquipmentSerializer(serializers.ModelSerializer):
#     contract = ContractDocumentSerializer(read_only=True, allow_null=True)
#     computer_details = ComputerDetailsSerializer(required=False, allow_null=True)
#     computer_specification_id = serializers.PrimaryKeyRelatedField(
#         queryset=ComputerSpecification.objects.all(),
#         required=False,
#         allow_null=True,
#         write_only=True,
#         help_text="ID шаблона компьютерной спецификации для автозаполнения характеристик"
#     )
#     PrinterChar = serializers.PrimaryKeyRelatedField(queryset=PrinterChar.objects.all(), required=False, allow_null=True)

#     computer_specification_data = ComputerSpecificationSerializer(source='computer_details', read_only=True, allow_null=True)
#     type = serializers.PrimaryKeyRelatedField(queryset=EquipmentType.objects.all())
#     type_data = EquipmentTypeSerializer(source='type', read_only=True)
#     room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), allow_null=True, required=False)
#     room_data = RoomSerializer(source='room', read_only=True, allow_null=True)
#     qr_code_url = serializers.SerializerMethodField()
#     author = UserSerializer(read_only=True)
#     author_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         write_only=True,
#         required=False,
#         allow_null=True,
#         source='author'
#     )

#     class Meta:
#         model = Equipment
#         fields = [
#             'id', 'type', 'type_data', 'room', 'room_data', 'name', 'photo', 'description',
#             'is_active', 'contract', 'created_at', 'computer_details', 'computer_specification_id',
#             'computer_specification_data', 'status', 'qr_code_url', 'uid', 'author', 'author_id', 'inn'
#         ]
#         read_only_fields = ['created_at', 'uid', 'author']

#     def get_qr_code_url(self, obj):
#         if obj.qr_code:
#             return obj.qr_code.url
#         return None

#     def validate(self, data):
#         equipment_type = data.get('type')
#         computer_details = data.get('computer_details')
#         computer_specification_id = data.get('computer_specification_id')

#         is_computer = equipment_type and equipment_type.name.lower() in ('компьютер', 'ноутбук', 'моноблок')

#         if is_computer and computer_details and computer_specification_id:
#             raise serializers.ValidationError(
#                 "Укажите либо computer_details, либо computer_specification_id, но не оба."
#             )
#         if not is_computer and (computer_details or computer_specification_id):
#             raise serializers.ValidationError(
#                 "Для этого типа оборудования компьютерные характеристики не поддерживаются."
#             )

#         return data

#     def create(self, validated_data):
#         computer_details_data = validated_data.pop('computer_details', None)
#         computer_specification = validated_data.pop('computer_specification_id', None)

#         # Получаем автора, если он передан или есть request
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             validated_data['author'] = request.user

#         equipment = Equipment.objects.create(**validated_data)

#         if equipment.type.name.lower() in ('компьютер', 'ноутбук', 'моноблок'):
#             if computer_specification:
#                 spec = computer_specification
#                 if not isinstance(computer_specification, ComputerSpecification):
#                     spec = ComputerSpecification.objects.get(id=computer_specification)

#                 computer_details_data = {
#                     'cpu': spec.cpu,
#                     'ram': spec.ram,
#                     'storage': spec.storage,
#                     'has_keyboard': spec.has_keyboard,
#                     'has_mouse': spec.has_mouse,
#                     'monitor_size': spec.monitor_size,
#                 }

#             if computer_details_data:
#                 ComputerDetails.objects.create(equipment=equipment, **computer_details_data)

#         return equipment


    def update(self, instance, validated_data):
        computer_details_data = validated_data.pop('computer_details', None)
        computer_specification_id = validated_data.pop('computer_specification_id', None)
        validated_data.pop('author', None)  # Запрещаем менять автора при обновлении

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instance.type.name.lower() == 'компьютер':
            if computer_specification_id:
                spec = ComputerSpecification.objects.get(id=computer_specification_id)
                computer_details_data = {
                    'cpu': spec.cpu,
                    'ram': spec.ram,
                    'storage': spec.storage,
                    'has_keyboard': spec.has_keyboard,
                    'has_mouse': spec.has_mouse,
                    'monitor_size': spec.monitor_size,
                }
            if computer_details_data:
                try:
                    computer_details = instance.computer_details
                    for attr, value in computer_details_data.items():
                        setattr(computer_details, attr, value)
                    computer_details.save()
                except ComputerDetails.DoesNotExist:
                    ComputerDetails.objects.create(equipment=instance, **computer_details_data)
        elif hasattr(instance, 'computer_details'):
            instance.computer_details.delete()

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


class MoveEquipmentSerializer(serializers.Serializer):
    equipment_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        required=True
    )
    from_room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        required=True
    )
    to_room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        required=True
    )

    def validate(self, data):
        equipment_ids = data['equipment_ids']
        from_room = data['from_room_id']
        to_room = data['to_room_id']

        # Проверяем, что оборудование существует и принадлежит from_room
        equipments = Equipment.objects.filter(id__in=equipment_ids, room=from_room)
        if equipments.count() != len(equipment_ids):
            raise serializers.ValidationError("Некоторые ID оборудования не найдены или не принадлежат указанному кабинету")

        # Проверяем, что from_room и to_room не совпадают
        if from_room == to_room:
            raise serializers.ValidationError("Исходный и целевой кабинеты должны быть разными")

        return data



# Массовая генерация оборудовании

class BulkEquipmentSerializer(serializers.Serializer):
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=EquipmentType.objects.all(),
        required=True
    )
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        required=False,
        allow_null=True
    )
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(
        choices=Equipment.STATUS_CHOICES,
        default='NEW'
    )
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=ContractDocument.objects.all(),
        required=False,
        allow_null=True
    )
    count = serializers.IntegerField(min_value=1, max_value=100, required=True)
    name_prefix = serializers.CharField(max_length=200, required=True)
    computer_details = ComputerDetailsSerializer(required=False, allow_null=True)
    computer_specification_id = serializers.PrimaryKeyRelatedField(
        queryset=ComputerSpecification.objects.all(),
        required=False,
        allow_null=True
    )
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    def validate(self, data):
        equipment_type = data.get('type_id')
        computer_details = data.get('computer_details')
        computer_specification_id = data.get('computer_specification_id')

        # Проверка типа оборудования
        is_computer = equipment_type and equipment_type.name.lower() == 'компьютер'
        if is_computer and computer_details and computer_specification_id:
            raise serializers.ValidationError(
                "Укажите либо computer_details, либо computer_specification_id, но не оба."
            )
        if not is_computer and (computer_details or computer_specification_id):
            raise serializers.ValidationError(
                "Для этого типа оборудования компьютерные характеристики не поддерживаются."
            )

        # Проверка существования комнаты
        if data.get('room_id') and not Room.objects.filter(id=data['room_id'].id).exists():
            raise serializers.ValidationError({"room_id": "Кабинет не найден"})

        return data

    def create(self, validated_data):
        count = validated_data.pop('count')
        name_prefix = validated_data.pop('name_prefix')
        computer_details_data = validated_data.pop('computer_details', None)
        computer_specification = validated_data.pop('computer_specification_id', None)
        author = validated_data.pop('author_id', None)
        request = self.context.get('request')

        # Устанавливаем автора
        if not author and request and request.user.is_authenticated:
            author = request.user

        equipments = []

        # Получаем данные спецификации, если указана
        if computer_specification:
            spec = computer_specification
            computer_details_data = {
                'cpu': spec.cpu,
                'ram': spec.ram,
                'storage': spec.storage,
                'has_keyboard': spec.has_keyboard,
                'has_mouse': spec.has_mouse,
                'monitor_size': spec.monitor_size,
            }

        for i in range(count):
            equipment_data = {
                'type': validated_data['type_id'],
                'room': validated_data.get('room_id'),
                'name': f"{name_prefix} {i + 1}",
                'description': validated_data.get('description', ''),
                'status': validated_data['status'],
                'contract': validated_data.get('contract_id'),
                'author': author,
                'inn': 0,  # ИНН будет задан на втором этапе
                'is_active': True
            }

            equipment = Equipment.objects.create(**equipment_data)

            if equipment.type.name.lower() == 'компьютер' and computer_details_data:
                ComputerDetails.objects.create(equipment=equipment, **computer_details_data)

            equipments.append(equipment)

        return equipments

class BulkEquipmentInnUpdateSerializer(serializers.Serializer):
    equipments = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            required=True
        ),
        min_length=1
    )

    def validate(self, data):
        equipment_data = data['equipments']
        equipment_ids = [item['id'] for item in equipment_data]
        inns = [item['inn'] for item in equipment_data]

        # Проверяем, что все ID существуют
        existing_equipments = Equipment.objects.filter(id__in=equipment_ids)
        if existing_equipments.count() != len(equipment_ids):
            raise serializers.ValidationError("Некоторые ID оборудования не найдены")

        # Проверяем, что все оборудования принадлежат текущему пользователю
        user = self.context['request'].user
        if existing_equipments.filter(author=user).count() != len(equipment_ids):
            raise serializers.ValidationError("Вы можете обновлять только своё оборудование")

        # Проверяем уникальность ИНН
        if len(inns) != len(set(inns)):
            raise serializers.ValidationError("ИНН должны быть уникальными")

        return data

    def update(self, validated_data):
        equipment_data = validated_data['equipments']
        equipments = []

        for item in equipment_data:
            equipment = Equipment.objects.get(id=item['id'])
            equipment.inn = item['inn']
            equipment.save()
            equipments.append(equipment)

        return equipments

import re
class EquipmentFromLinkSerializer(serializers.Serializer):
    room_link = serializers.URLField(required=True)

    def validate_room_link(self, value):
        match = re.match(r'.*/rooms/(\d+)/\?building=(\d+)', value)
        if not match:
            raise serializers.ValidationError("Неверный формат ссылки")
        room_id, building_id = match.groups()
        try:
            room = Room.objects.get(id=room_id, building_id=building_id)
        except Room.DoesNotExist:
            raise serializers.ValidationError("Кабинет или корпус не найдены")
        return {'room_id': room_id, 'building_id': building_id, 'room': room}