from django.urls import path
from . import views

urlpatterns = [
    # Университеты
    path('universities/', views.UniversityListCreateView.as_view(), name='university-list-create'),
    path('universities/<int:pk>/', views.UniversityDetailView.as_view(), name='university-detail'),

    # Корпуса
    path('buildings/', views.BuildingListCreateView.as_view(), name='building-list-create'),
    path('buildings/<int:pk>/', views.BuildingDetailView.as_view(), name='building-detail'),

    # Факультеты
    path('faculties/', views.FacultyListCreateView.as_view(), name='faculty-list-create'),
    path('faculties/<int:pk>/', views.FacultyDetailView.as_view(), name='faculty-detail'),

    # Этажи
    path('floors/', views.FloorListCreateView.as_view(), name='floor-list-create'),
    path('floors/<int:pk>/', views.FloorDetailView.as_view(), name='floor-detail'),

    # Кабинеты
    path('rooms/', views.RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),

    # Кафедры
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
]
