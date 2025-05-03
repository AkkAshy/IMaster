from rest_framework import serializers
from .models import University, Building, Faculty, Floor, Room, Department, RoomHistory
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
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'number', 'name', 'is_special', 'photo', 'qr_code', 'qr_code_url', 'floor']


    def create(self, validated_data):
        room = Room(**validated_data)
        room.save()  # Здесь уже сработает метод модели save()
        return room
    
    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None

class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    class Meta:
        model = Department
        fields = ['id', 'name', 'faculty']

class RoomHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomHistory
        fields = ['id', 'room', 'action', 'timestamp', 'description']
