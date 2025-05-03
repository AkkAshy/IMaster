from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipmentTypeViewSet, ContractDocumentViewSet, EquipmentViewSet,
    ComputerDetailsViewSet, MovementHistoryViewSet
)

router = DefaultRouter()
router.register(r'equipment-types', EquipmentTypeViewSet, basename='equipment-type')
router.register(r'contracts', ContractDocumentViewSet, basename='contract')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'computer-details', ComputerDetailsViewSet, basename='computer-details')
router.register(r'movement-history', MovementHistoryViewSet, basename='movement-history')

urlpatterns = [
    path('', include(router.urls)),
]