from rest_framework import generics
from .models import University, Building, Faculty, Floor, Room, Department
from .serializers import UniversitySerializer, BuildingSerializer, FacultySerializer, FloorSerializer, RoomSerializer, DepartmentSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser


# Университеты
class UniversityListCreateView(generics.ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

# Корпуса
class BuildingListCreateView(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]

class BuildingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]

# Факультеты
class FacultyListCreateView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]

class FacultyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]

# Этажи
class FloorListCreateView(generics.ListCreateAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]

class FloorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]

class FloorByBuildingView(generics.ListAPIView):
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Floor.objects.filter(building_id=self.kwargs['building_pk'])
    

# Кабинеты
class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

# Кафедры
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
