from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import EquipmentType, ContractDocument, Equipment, ComputerDetails, MovementHistory
from .serializers import (
    EquipmentTypeSerializer, ContractDocumentSerializer, EquipmentSerializer,
    ComputerDetailsSerializer, MovementHistorySerializer
)


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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description', 'inn']
    filterset_fields = ['type', 'room', 'is_active']

    @action(detail=True, methods=['get'])
    def movements(self, request, pk=None):
        equipment = self.get_object()
        movements = equipment.movements.all()
        serializer = MovementHistorySerializer(movements, many=True)
        return Response(serializer.data)


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