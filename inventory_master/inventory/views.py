# from rest_framework import viewsets, generics
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.filters import SearchFilter
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.views import APIView
# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.db import transaction
# from django_filters.rest_framework import DjangoFilterBackend
# from .qr_serializations import QRScanSerializer

# from university.models import Room, Building
# from university.serializers import RoomSerializer


# from user.models import UserAction
# from user.serializers import UserActionSerializer


# from .models import (EquipmentType, ContractDocument, Equipment,
#                      ComputerDetails, MovementHistory, ComputerSpecification,
#                      TVChar, ExtenderChar, RouterChar, PrinterChar,
#                      PrinterSpecification, ExtenderSpecification,
#                      RouterSpecification, TVSpecification
# )

# from .serializers import (
#     EquipmentTypeSerializer, ContractDocumentSerializer, EquipmentSerializer,
#     ComputerDetailsSerializer, MovementHistorySerializer, ComputerSpecificationSerializer,
#     MoveEquipmentSerializer, BulkEquipmentSerializer, BulkEquipmentInnUpdateSerializer,
#     PrinterCharSerializer, ExtenderCharSerializer, TVCharSerializer, RouterCharSerializer,
#     PrinterSpecificationSerializer, ExtenderSpecificationSerializer,
#     RouterSpecificationSerializer, TVSpecificationSerializer
# )

# from .qr_serializations import QRScanSerializer




# class EquipmentTypeViewSet(viewsets.ModelViewSet):
#     queryset = EquipmentType.objects.all()
#     serializer_class = EquipmentTypeSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     search_fields = ['name']
#     filterset_fields = ['name']


# class ContractDocumentViewSet(viewsets.ModelViewSet):
#     queryset = ContractDocument.objects.all()
#     serializer_class = ContractDocumentSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     search_fields = ['number']
#     filterset_fields = ['created_at']


# class EquipmentViewSet(viewsets.ModelViewSet):
#     queryset = Equipment.objects.all()
#     serializer_class = EquipmentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Equipment.objects.filter(author=self.request.user)




#     def perform_create(self, serializer):
#         equipment = serializer.save(author=self.request.user)
#         # Логируем создание одного оборудования
#         UserAction.objects.create(
#             user=self.request.user,
#             action_type='SINGLE_CREATE',
#             description=f"Создано оборудование: {equipment.name}"
#         )

#     @action(detail=False, methods=['post'], url_path='scan-qr')
#     def scan_qr(self, request):
#         serializer = QRScanSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)

#         # validated_data теперь выглядит как:
#         # {
#         #     'type': 'room' или 'equipment',
#         #     'data': { ... },
#         #     'equipments': [ ... ]  <- только если тип room
#         # }

#         return Response(serializer.validated_data)

#     @action(detail=False, methods=['post'], url_path='bulk-create')
#     @transaction.atomic
#     def bulk_create(self, request):
#         serializer = BulkEquipmentSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             equipments = serializer.create(serializer.validated_data)
#             # Логируем действие
#             UserAction.objects.create(
#                 user=request.user,
#                 action_type='CREATE',
#                 description=f"Создано {len(equipments)} оборудования с префиксом {serializer.validated_data['name_prefix']}"
#             )
#             return Response(EquipmentSerializer(equipments, many=True).data, status=201)
#         return Response(serializer.errors, status=400)

#     @action(detail=False, methods=['post'], url_path='bulk-update-inn')
#     @transaction.atomic
#     def bulk_update_inn(self, request):
#         serializer = BulkEquipmentInnUpdateSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             equipments = serializer.update(serializer.validated_data)
#             # Логируем действие
#             UserAction.objects.create(
#                 user=request.user,
#                 action_type='UPDATE_INN',
#                 description=f"Обновлены ИНН для {len(equipments)} оборудования"
#             )
#             return Response(EquipmentSerializer(equipments, many=True).data)
#         return Response(serializer.errors, status=400)

#     @action(detail=False, methods=['post'], url_path='move-equipment')
#     @transaction.atomic
#     def move_equipment(self, request):
#         serializer = MoveEquipmentSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             equipment_ids = serializer.validated_data['equipment_ids']
#             from_room = serializer.validated_data['from_room_id']
#             to_room = serializer.validated_data['to_room_id']
#             equipments = Equipment.objects.filter(id__in=equipment_ids, room=from_room, author=self.request.user)
#             for equipment in equipments:
#                 MovementHistory.objects.create(
#                     equipment=equipment,
#                     from_room=from_room,
#                     to_room=to_room
#                 )
#                 equipment.room = to_room
#                 equipment.save()
#             # Логируем действие
#             UserAction.objects.create(
#                 user=request.user,
#                 action_type='MOVE',
#                 description=f"Перемещено {equipments.count()} оборудования из кабинета {from_room.number} в кабинет {to_room.number}"
#             )
#             return Response({'message': f'Оборудование перемещено из кабинета {from_room.number} в кабинет {to_room.number}'})
#         return Response(serializer.errors, status=400)

#     @action(detail=False, methods=['get'], url_path=r'rooms-by-building/(?P<building_id>\d+)')
#     def rooms_by_building(self, request, building_id=None):
#         rooms = Room.objects.filter(building_id=building_id)
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'], url_path=r'equipment-by-room/(?P<room_id>\d+)')
#     def equipment_by_room(self, request, room_id=None):
#         equipments = Equipment.objects.filter(room_id=room_id, author=self.request.user)
#         serializer = EquipmentSerializer(equipments, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'], url_path='my-actions')
#     def my_actions(self, request):
#         actions = UserAction.objects.filter(user=request.user)[:10]  # Последние 10 действий
#         serializer = UserActionSerializer(actions, many=True)
#         return Response(serializer.data)



# class ComputerSpecificationListView(generics.ListAPIView):
#     queryset = ComputerSpecification.objects.all()
#     serializer_class = ComputerSpecificationSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     search_fields = ['cpu', 'ram', 'storage']

#     def get_queryset(self):
#         # Фильтруем записи по текущему пользователю
#         return ComputerSpecification.objects.filter(author=self.request.user)

#     def perform_create(self, serializer):
#         # Автоматически устанавливаем текущего пользователя как автора
#         serializer.save(author=self.request.user)



# class ComputerSpecificationCreateView(generics.CreateAPIView):
#     queryset = ComputerSpecification.objects.all()
#     serializer_class = ComputerSpecificationSerializer
#     permission_classes = [IsAuthenticated]



# class ComputerDetailsViewSet(viewsets.ModelViewSet):
#     queryset = ComputerDetails.objects.all()
#     serializer_class = ComputerDetailsSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['has_keyboard', 'has_mouse']


# class MovementHistoryViewSet(viewsets.ModelViewSet):
#     queryset = MovementHistory.objects.all()
#     serializer_class = MovementHistorySerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     search_fields = ['equipment__name']
#     filterset_fields = ['equipment', 'from_room', 'to_room', 'moved_at']

#     def perform_create(self, serializer):
#         movement = serializer.save()
#         if movement.to_room:
#             movement.equipment.room = movement.to_room
#             movement.equipment.save()



# class PrinterCharViewSet(viewsets.ModelViewSet):
#     queryset = PrinterChar.objects.all()
#     serializer_class = PrinterCharSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name', 'model']
#     search_fields = ['name', 'model']
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         return PrinterCharSerializer.objects.filter(author=self.request.user)
#     def perform_create(self, serializer):
#         printer = serializer.save(author=self.request.user)
#         # Логируем создание одного оборудования
#         UserAction.objects.create(
#             user=self.request.user,
#             action_type='SINGLE_CREATE',
#             description=f"Создан принтер: {printer.name}"
#         )

# class ExtenderCharViewSet(viewsets.ModelViewSet):
#     queryset = ExtenderChar.objects.all()
#     serializer_class = ExtenderCharSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name', 'model']
#     search_fields = ['name', 'model']
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         return ExtenderCharSerializer.objects.filter(author=self.request.user)
#     def perform_create(self, serializer):
#         extender = serializer.save(author=self.request.user)
#         # Логируем создание одного оборудования
#         UserAction.objects.create(
#             user=self.request.user,
#             action_type='SINGLE_CREATE',
#             description=f"Создан удлинитель: {extender.name}"
#         )
# class TVCharViewSet(viewsets.ModelViewSet):
#     queryset = TVChar.objects.all()
#     serializer_class = TVCharSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name', 'model']
#     search_fields = ['name', 'model']
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         return TVCharSerializer.objects.filter(author=self.request.user)
#     def perform_create(self, serializer):
#         tv = serializer.save(author=self.request.user)
#         # Логируем создание одного оборудования
#         UserAction.objects.create(
#             user=self.request.user,
#             action_type='SINGLE_CREATE',
#             description=f"Создан телевизор: {tv.name}"
#         )

# class RouterCharViewSet(viewsets.ModelViewSet):
#     queryset = RouterChar.objects.all()
#     serializer_class = RouterCharSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name', 'model']
#     search_fields = ['name', 'model']
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         return RouterCharSerializer.objects.filter(author=self.request.user)
#     def perform_create(self, serializer):
#         router = serializer.save(author=self.request.user)
#         # Логируем создание одного оборудования
#         UserAction.objects.create(
#             user=self.request.user,
#             action_type='SINGLE_CREATE',
#             description=f"Создан роутер: {router.name}"
#         )


# # ViewSet для спецификаций
# class PrinterSpecificationViewSet(ModelViewSet):
#     serializer_class = PrinterSpecificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return PrinterSpecification.objects.filter(author=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# class ExtenderSpecificationViewSet(ModelViewSet):
#     serializer_class = ExtenderSpecificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return ExtenderSpecification.objects.filter(author=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# class RouterSpecificationViewSet(ModelViewSet):
#     serializer_class = RouterSpecificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return RouterSpecification.objects.filter(author=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# class TVSpecificationViewSet(ModelViewSet):
#     serializer_class = TVSpecificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return TVSpecification.objects.filter(author=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# from user.models import UserAction


# class QRScanView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = QRScanSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             object_type = serializer.validated_data['object_type']
#             obj_data = serializer.validated_data['object']
#             UserAction.objects.create(
#                 user=request.user,
#                 action_type='SCAN',
#                 description=f"Отсканирован QR-код: {object_type}"
#             )
#             return Response({
#                 'type': object_type,
#                 'data': obj_data
#             })
#         return Response(serializer.errors, status=400)


from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .qr_serializations import QRScanSerializer



from university.models import Room, Building
from university.serializers import RoomSerializer


from user.models import UserAction
from user.serializers import UserActionSerializer


from .models import (EquipmentType, ContractDocument, Equipment,
                     ComputerDetails, MovementHistory, ComputerSpecification,
                     TVChar, ExtenderChar, RouterChar, PrinterChar,
                     PrinterSpecification, ExtenderSpecification,
                     RouterSpecification, TVSpecification,
                    WhiteboardSpecification, WhiteboardChar,
                    ProjectorChar, ProjectorSpecification,
                    NotebookChar, NotebookSpecification,
                    MonoblokChar, MonoblokSpecification
)

from .serializers import (
    EquipmentTypeSerializer, ContractDocumentSerializer, EquipmentSerializer,
    ComputerDetailsSerializer, MovementHistorySerializer, ComputerSpecificationSerializer,
    MoveEquipmentSerializer, BulkEquipmentSerializer, BulkEquipmentInnUpdateSerializer,
    PrinterCharSerializer, ExtenderCharSerializer, TVCharSerializer, RouterCharSerializer,
    PrinterSpecificationSerializer, ExtenderSpecificationSerializer,
    RouterSpecificationSerializer, TVSpecificationSerializer,
    MonoblokCharSerializer, MonoblokSpecificationSerializer,
    NotebookCharSerializer, NotebookSpecificationSerializer,
    ProjectorCharSerializer, ProjectorSpecificationSerializer,
    WhiteboardCharSerializer, WhiteboardSpecificationSerializer,
    EquipmentFromLinkSerializer
)



from django.urls import reverse

class EquipmentFromLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EquipmentFromLinkSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            room_data = serializer.validated_data['room_link']
            room_id = room_data['room_id']
            building_id = room_data['building_id']
            equipment_data = serializer.validated_data.get('equipment_data')

            if equipment_data:
                # Прямое создание оборудования
                equipment_data['room'] = room_data['room']
                equipment_serializer = EquipmentSerializer(data=equipment_data, context={'request': request})
                if equipment_serializer.is_valid():
                    equipment = equipment_serializer.save(author=request.user)
                    UserAction.objects.create(
                        user=request.user,
                        action_type='SINGLE_CREATE',
                        description=f"Создано оборудование: {equipment.name}"
                    )
                    return Response(equipment_serializer.data, status=201)
                return Response(equipment_serializer.errors, status=400)

            # Возврат данных для формы
            return Response({
                'room_id': room_id,
                'building_id': building_id,
                'create_url': request.build_absolute_uri(
                    f"{reverse('equipment-list')}?room={room_id}&building={building_id}"
                ),
                'form_fields': {
                    'room': room_id,
                    'building': building_id,
                    'equipment_types': list(EquipmentType.objects.values('id', 'name')),
                    'status_choices': Equipment.STATUS_CHOICES
                }
            })
        return Response(serializer.errors, status=400)

class EquipmentTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['name']


class ContractDocumentViewSet(viewsets.ModelViewSet):
    queryset = ContractDocument.objects.all()
    serializer_class = ContractDocumentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['number']
    filterset_fields = ['created_at']


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Equipment.objects.filter(author=self.request.user)




    def perform_create(self, serializer):
        equipment = serializer.save(author=self.request.user)
        # Логируем создание одного оборудования
        UserAction.objects.create(
            user=self.request.user,
            action_type='SINGLE_CREATE',
            description=f"Создано оборудование: {equipment.name}"
        )

    @action(detail=False, methods=['post'], url_path='scan-qr')
    def scan_qr(self, request):
        serializer = QRScanSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # validated_data теперь выглядит как:
        # {
        #     'type': 'room' или 'equipment',
        #     'data': { ... },
        #     'equipments': [ ... ]  <- только если тип room
        # }

        return Response(serializer.validated_data)

    @action(detail=False, methods=['post'], url_path='bulk-create')
    @transaction.atomic
    def bulk_create(self, request):
        serializer = BulkEquipmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            equipments = serializer.create(serializer.validated_data)

            name_prefix = serializer.validated_data.get('name_prefix', '[без префикса]')

            # Логируем действие
            UserAction.objects.create(
                user=request.user,
                action_type='CREATE',
                description=f"Создано {len(equipments)} оборудования с префиксом {name_prefix}"
            )
            return Response(EquipmentSerializer(equipments, many=True).data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], url_path='bulk-update-inn')
    @transaction.atomic
    def bulk_update_inn(self, request):
        serializer = BulkEquipmentInnUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            equipments = serializer.update(serializer.validated_data) or []
            count = len(equipments) if hasattr(equipments, '__len__') else 1
            UserAction.objects.create(
                user=request.user,
                action_type='UPDATE_INN',
                description=f"Обновлены ИНН для {count} оборудования"
            )
            return Response(EquipmentSerializer(equipments, many=True).data)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], url_path='move-equipment')
    @transaction.atomic
    def move_equipment(self, request):
        serializer = MoveEquipmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            equipment_ids = serializer.validated_data.get('equipment_ids', [])
            from_room = serializer.validated_data.get('from_room_id')
            to_room = serializer.validated_data.get('to_room_id')

            if not from_room or not to_room:
                return Response({'detail': 'Неверные данные комнат.'}, status=400)

            equipments = Equipment.objects.filter(id__in=equipment_ids, room=from_room, author=self.request.user)
            for equipment in equipments:
                MovementHistory.objects.create(
                    equipment=equipment,
                    from_room=from_room,
                    to_room=to_room
                )
                equipment.room = to_room
                equipment.save()

            UserAction.objects.create(
                user=request.user,
                action_type='MOVE',
                description=f"Перемещено {equipments.count()} оборудования из кабинета {from_room.number} в кабинет {to_room.number}"
            )
            return Response({'message': f'Оборудование перемещено из кабинета {from_room.number} в кабинет {to_room.number}'})
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'], url_path=r'rooms-by-building/(?P<building_id>\d+)')
    def rooms_by_building(self, request, building_id=None):
        rooms = Room.objects.filter(building_id=building_id)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'equipment-by-room/(?P<room_id>\d+)')
    def equipment_by_room(self, request, room_id=None):
        equipments = Equipment.objects.filter(room_id=room_id, author=self.request.user)
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-equipments')
    def my_equipments(self, request):
        equipments = self.get_queryset()
        serializer = self.get_serializer(equipments, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='my-actions')
    def my_actions(self, request):
        actions = UserAction.objects.filter(user=request.user)[:10]  # Последние 10 действий
        serializer = UserActionSerializer(actions, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path=r'by-room/(?P<room_id>\d+)/types')
    def equipment_by_type(self, request, room_id=None):
        # Проверяем существование комнаты
        room = get_object_or_404(Room, id=room_id)

        # Маппинг имён типов
        TYPE_NAME_MAPPING = {
            'компьютер': 'Computer',
            'ноутбук': 'Laptop',
            'моноблок': 'Monoblock',
            'принтер': 'Printer',
            'удлинитель': 'ExtensionCord',
            'электронная доска': 'InteractiveBoard',
            'проектор': 'Projector',
            'тв': 'TV',
            'роутер': 'Router'
        }

        # Получаем оборудование в комнате, оптимизируя запрос
        equipments = Equipment.objects.filter(
            room_id=room_id,
            author=self.request.user
        ).select_related('type')

        # Инициализируем результат с сериализованными данными
        result = {mapped_name: [] for mapped_name in TYPE_NAME_MAPPING.values()}
        for equipment in equipments:
            type_name = equipment.type.name.lower()
            key = TYPE_NAME_MAPPING.get(type_name, type_name)
            serializer = EquipmentSerializer(equipment)
            result[key].append(serializer.data)


        result = {key: value for key, value in result.items() if value}

        # Если ничего не найдено, возвращаем пустой объект
        if not result:
            return Response({"detail": "Оборудование не найдено"}, status=200)

        return Response(result)


class ComputerSpecificationListView(generics.ListCreateAPIView):
    queryset = ComputerSpecification.objects.all()
    serializer_class = ComputerSpecificationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['cpu', 'ram', 'storage']

    def get_queryset(self):
        # Фильтруем записи по текущему пользователю
        return ComputerSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как автора
        serializer.save(author=self.request.user)



class ComputerSpecificationCreateView(generics.CreateAPIView):
    queryset = ComputerSpecification.objects.all()
    serializer_class = ComputerSpecificationSerializer
    permission_classes = [IsAuthenticated]



class ComputerDetailsViewSet(viewsets.ModelViewSet):
    queryset = ComputerDetails.objects.all()
    serializer_class = ComputerDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['has_keyboard', 'has_mouse']


class MovementHistoryViewSet(viewsets.ModelViewSet):
    queryset = MovementHistory.objects.all()
    serializer_class = MovementHistorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['equipment__name']
    filterset_fields = ['equipment', 'from_room', 'to_room', 'moved_at']

    def perform_create(self, serializer):
        movement = serializer.save()
        if movement.to_room:
            movement.equipment.room = movement.to_room
            movement.equipment.save()



class PrinterCharViewSet(viewsets.ModelViewSet):
    queryset = PrinterChar.objects.all()
    serializer_class = PrinterCharSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'model']
    search_fields = ['name', 'model']
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return PrinterCharSerializer.objects.filter(author=self.request.user)
    def perform_create(self, serializer):
        printer = serializer.save(author=self.request.user)
        # Логируем создание одного оборудования
        UserAction.objects.create(
            user=self.request.user,
            action_type='SINGLE_CREATE',
            description=f"Создан принтер: {printer.name}"
        )

class ExtenderCharViewSet(viewsets.ModelViewSet):
    queryset = ExtenderChar.objects.all()
    serializer_class = ExtenderCharSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'model']
    search_fields = ['name', 'model']
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ExtenderCharSerializer.objects.filter(author=self.request.user)
    def perform_create(self, serializer):
        extender = serializer.save(author=self.request.user)
        # Логируем создание одного оборудования
        UserAction.objects.create(
            user=self.request.user,
            action_type='SINGLE_CREATE',
            description=f"Создан удлинитель: {extender.name}"
        )
class TVCharViewSet(viewsets.ModelViewSet):
    queryset = TVChar.objects.all()
    serializer_class = TVCharSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'model']
    search_fields = ['name', 'model']
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return TVCharSerializer.objects.filter(author=self.request.user)
    def perform_create(self, serializer):
        tv = serializer.save(author=self.request.user)
        # Логируем создание одного оборудования
        UserAction.objects.create(
            user=self.request.user,
            action_type='SINGLE_CREATE',
            description=f"Создан телевизор: {tv.name}"
        )

class RouterCharViewSet(viewsets.ModelViewSet):
    queryset = RouterChar.objects.all()
    serializer_class = RouterCharSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'model']
    search_fields = ['name', 'model']
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return RouterCharSerializer.objects.filter(author=self.request.user)
    def perform_create(self, serializer):
        router = serializer.save(author=self.request.user)
        # Логируем создание одного оборудования
        UserAction.objects.create(
            user=self.request.user,
            action_type='SINGLE_CREATE',
            description=f"Создан роутер: {router.name}"
        )


# ViewSet для спецификаций
class PrinterSpecificationViewSet(ModelViewSet):
    serializer_class = PrinterSpecificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PrinterSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ExtenderSpecificationViewSet(ModelViewSet):
    serializer_class = ExtenderSpecificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExtenderSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RouterSpecificationViewSet(ModelViewSet):
    serializer_class = RouterSpecificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RouterSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TVSpecificationViewSet(ModelViewSet):
    serializer_class = TVSpecificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TVSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

######################################################################
class ProjectorCharViewSet(ModelViewSet):
    serializer_class = ProjectorCharSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProjectorChar.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ProjectorSpecificationViewSet(ModelViewSet):
    serializer_class = ProjectorSpecificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProjectorSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class WhiteboardCharViewSet(ModelViewSet):
    serializer_class = WhiteboardCharSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WhiteboardChar.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class WhiteboardSpecificationViewSet(ModelViewSet):
    serializer_class = WhiteboardSpecificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WhiteboardSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NotebookCharViewSet(ModelViewSet):
    serializer_class = NotebookCharSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotebookChar.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NotebookSpecificationViewSet(ModelViewSet):
    serializer_class = NotebookSpecificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotebookSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class MonoblokCharViewSet(ModelViewSet):
    serializer_class = MonoblokCharSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MonoblokChar.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class MonoblokSpecificationViewSet(ModelViewSet):
    serializer_class = MonoblokSpecificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MonoblokSpecification.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QRScanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QRScanSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            object_type = serializer.validated_data['object_type']
            obj_data = serializer.validated_data['object']
            UserAction.objects.create(
                user=request.user,
                action_type='SCAN',
                description=f"Отсканирован QR-код: {object_type}"
            )
            return Response({
                'type': object_type,
                'data': obj_data
            })
        return Response(serializer.errors, status=400)