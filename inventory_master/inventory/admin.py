from django.contrib import admin
from .models import EquipmentType, Equipment, ComputerDetails, MovementHistory, ContractDocument
from university.models import Room
from inventory.models import Equipment
from django import forms
from django.shortcuts import render, redirect
from django.urls import path

class MoveEquipmentForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    new_room = forms.ModelChoiceField(queryset=Room.objects.all(), label="Выбери новый кабинет")

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'get_room_name', 'is_active', 'created_at')
    search_fields = ['name', 'description', 'inn']
    list_filter = ('is_active',)
    actions = ['move_equipment']
    

    def get_room_name(self, obj):
        print(f"Room ID: {obj.room.id}, Number: {obj.room.number}, Name: {obj.room.name}")
        return obj.room.number 
    get_room_name.short_description = "Номер кабинета"

    def move_equipment(self, request, queryset):
        # Смотрим, выбран ли кабинет для перемещения
        if 'apply' in request.POST:
            room_id = request.POST.get('to_room')
            to_room = Room.objects.get(id=room_id)
            for equipment in queryset:
                # Создаем запись в истории перемещений
                MovementHistory.objects.create(
                    equipment=equipment,
                    from_room=equipment.room,
                    to_room=to_room
                )
                # Обновляем кабинет оборудования
                equipment.room = to_room
                equipment.save()
            self.message_user(request, "Оборудование перемещено.")
            return redirect('..')

        # Если еще не выбрали кабинет, показываем форму для выбора
        return render(
            request,
            'admin/move_equipment.html',  # Создадим кастомный шаблон
            {'equipments': queryset, 'rooms': Room.objects.all()}
        )
    
    move_equipment.short_description = "Переместить оборудование"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('move_equipment/', self.move_equipment, name='move_equipment'),
        ]
        return custom_urls + urls

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ComputerDetails)
class ComputerDetailsAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'cpu', 'ram', 'storage', 'has_keyboard', 'has_mouse', 'monitor_size')

@admin.register(MovementHistory)
class MovementHistoryAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'from_room', 'to_room', 'moved_at')
    list_filter = ('moved_at',)

@admin.register(ContractDocument)
class ContractDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'file', 'created_at')