from django.contrib import admin
from .models import University, Building, Faculty, Floor, Room, Department


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'address')
    list_filter = ('university',)
    search_fields = ('name', 'address')
    list_per_page = 20


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'building')
    list_filter = ('building',)
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('number', 'building', 'description')
    list_filter = ('building',)
    search_fields = ('description',)
    list_per_page = 20


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ('qr_code_preview',)
    fields = ('floor', 'number', 'name', 'is_special', 'photo', 'qr_code_preview')

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return f'<img src="{obj.qr_code.url}" width="150" height="150" />'
        return "(QR-код не сгенерирован)"
    qr_code_preview.short_description = "QR-код"
    qr_code_preview.allow_tags = True


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    list_filter = ('faculty',)
    search_fields = ('name',)
    list_per_page = 20
