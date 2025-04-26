from rest_framework import serializers
from .models import University, Building, Faculty, Floor, Room, Department
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'address', 'logo']

class BuildingSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = Building
        fields = ['id', 'name', 'address', 'photo', 'university']

class FacultySerializer(serializers.ModelSerializer):
    building = serializers.PrimaryKeyRelatedField(queryset=Building.objects.all())

    class Meta:
        model = Faculty
        fields = ['id', 'name', 'photo', 'building']

class FloorSerializer(serializers.ModelSerializer):
    building = serializers.PrimaryKeyRelatedField(queryset=Building.objects.all())

    class Meta:
        model = Floor
        fields = ['id', 'number', 'description', 'building']

class RoomSerializer(serializers.ModelSerializer):
    floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all())
    qr_code = serializers.ImageField(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'number', 'name', 'is_special', 'photo', 'qr_code', 'floor']

    def create(self, validated_data):
        # QR код создается автоматически через сигнал
        room = Room.objects.create(**validated_data)
        return room

class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(qeryset=Faculty.objects.all())
    class Meta:
        model = Department
        fields = ['id', 'name', 'faculty']
