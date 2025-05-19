from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipmentTypeViewSet, ContractDocumentViewSet, EquipmentViewSet,
    ComputerDetailsViewSet, MovementHistoryViewSet, ComputerSpecificationListView,
    ComputerSpecificationCreateView, RouterCharViewSet, PrinterCharViewSet,
    TVCharViewSet, PrinterSpecificationViewSet, ExtenderCharViewSet,
    ExtenderSpecificationViewSet, TVSpecificationViewSet, RouterSpecificationViewSet,
    EquipmentFromLinkView, QRScanView,
    ProjectorCharViewSet, ProjectorSpecificationViewSet,
    WhiteboardCharViewSet, WhiteboardSpecificationViewSet,
    MonoblokCharViewSet, MonoblokSpecificationViewSet,
    NotebookCharViewSet, NotebookSpecificationViewSet
)

router = DefaultRouter()
router.register(r'equipment-types', EquipmentTypeViewSet, basename='equipment-type')
router.register(r'contracts', ContractDocumentViewSet, basename='contract')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'computer-details', ComputerDetailsViewSet, basename='computer-details')
router.register(r'movement-history', MovementHistoryViewSet, basename='movement-history')
router.register(r'router-char', RouterCharViewSet, basename='router-char')
router.register(r'printer-char', PrinterCharViewSet, basename='printer-char')
router.register(r'tv-char', TVCharViewSet, basename='tv-char')
router.register(r'extender-char', ExtenderCharViewSet, basename='extender-char')
router.register(r'printer-specification', PrinterSpecificationViewSet, basename='printer-specification')
router.register(r'extender-specification', ExtenderSpecificationViewSet, basename='extender-specification')
router.register(r'tv-specification', TVSpecificationViewSet, basename='tv-specification')
router.register(r'router-specification', RouterSpecificationViewSet, basename='router-specification')

router.register(r'projector-char', ProjectorCharViewSet, basename='projector-char')
router.register(r'projector-specification', ProjectorSpecificationViewSet, basename='projector-specification')
router.register(r'whiteboard-char', WhiteboardCharViewSet, basename='whiteboard-char')
router.register(r'whiteboard-specification', WhiteboardSpecificationViewSet, basename='whiteboard-specification')
router.register(r'monoblok-char', MonoblokCharViewSet, basename='monoblok-char')
router.register(r'monoblok-specification', MonoblokSpecificationViewSet, basename='monoblok-specification')
router.register(r'notebook-char', NotebookCharViewSet, basename='notebook-char')
router.register(r'notebook-specification', NotebookSpecificationViewSet, basename='notebook-specification')





urlpatterns = [
    path('', include(router.urls)),
    path('computer-specifications/', ComputerSpecificationListView.as_view(), name='computer-specifications-list'),
    path('', QRScanView.as_view(), name='scan-qr'),
    path('create-comp-spec/', ComputerSpecificationCreateView.as_view(), name='create-computer-spec'),
    path('from-link/', EquipmentFromLinkView.as_view(), name='equipment-from-link'),

]