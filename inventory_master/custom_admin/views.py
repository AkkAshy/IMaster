from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from university.models import Room, Floor, Building, University, Faculty, Department
from inventory.models import Equipment, ContractDocument, EquipmentType, ComputerDetails, MovementHistory
from user.models import User
from .forms import (RoomForm, EquipmentForm, ContractDocumentForm, UniversityForm,
                    BuildingForm, FacultyForm, FloorForm, DepartmentForm, UserForm, MovementForm, EquipmentTypeForm)

# Проверяем, что пользователь — ADMIN или MANAGER
class AdminOrManagerMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('custom_admin:login')
        if not (request.user.is_admin() or request.user.is_manager()):
            return render(request, 'custom_admin/error.html', {
                'error': 'Доступ только для администраторов или менеджеров'
            }, status=403)
        return super().dispatch(request, *args, **kwargs)

# Дашборд
class DashboardView(AdminOrManagerMixin, TemplateView):
    template_name = 'custom_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_count'] = University.objects.count()
        context['building_count'] = Building.objects.count()
        context['faculty_count'] = Faculty.objects.count()
        context['floor_count'] = Floor.objects.count()
        context['room_count'] = Room.objects.count()
        context['department_count'] = Department.objects.count()
        context['equipment_count'] = Equipment.objects.count()
        context['contract_count'] = ContractDocument.objects.count()
        context['user_count'] = User.objects.count()
        context['movement_count'] = MovementHistory.objects.count()
        return context

# Логин
class LoginView(View):
    template_name = 'custom_admin/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('custom_admin:dashboard')
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('custom_admin:dashboard')
        return render(request, self.template_name, {'form': form})

# Логаут
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('custom_admin:login')

# Университеты
class UniversityListView(AdminOrManagerMixin, ListView):
    model = University
    template_name = 'custom_admin/university_list.html'
    context_object_name = 'universities'
    paginate_by = 10

class UniversityCreateView(AdminOrManagerMixin, CreateView):
    model = University
    form_class = UniversityForm
    template_name = 'custom_admin/university_form.html'
    success_url = reverse_lazy('custom_admin:university_list')

class UniversityUpdateView(AdminOrManagerMixin, UpdateView):
    model = University
    form_class = UniversityForm
    template_name = 'custom_admin/university_form.html'
    success_url = reverse_lazy('custom_admin:university_list')

class UniversityDeleteView(AdminOrManagerMixin, DeleteView):
    model = University
    template_name = 'custom_admin/university_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:university_list')

# Корпуса
class BuildingListView(AdminOrManagerMixin, ListView):
    model = Building
    template_name = 'custom_admin/building_list.html'
    context_object_name = 'buildings'
    paginate_by = 10

    def get_queryset(self):
        queryset = Building.objects.all().select_related('university')
        university_id = self.request.GET.get('university')
        if university_id:
            queryset = queryset.filter(university_id=university_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['universities'] = University.objects.all()
        return context

class BuildingCreateView(AdminOrManagerMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'custom_admin/building_form.html'
    success_url = reverse_lazy('custom_admin:building_list')

class BuildingUpdateView(AdminOrManagerMixin, UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'custom_admin/building_form.html'
    success_url = reverse_lazy('custom_admin:building_list')

class BuildingDeleteView(AdminOrManagerMixin, DeleteView):
    model = Building
    template_name = 'custom_admin/building_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:building_list')

# Факультеты
class FacultyListView(AdminOrManagerMixin, ListView):
    model = Faculty
    template_name = 'custom_admin/faculty_list.html'
    context_object_name = 'faculties'
    paginate_by = 10

    def get_queryset(self):
        queryset = Faculty.objects.all().select_related('building__university')
        building_id = self.request.GET.get('building')
        if building_id:
            queryset = queryset.filter(building_id=building_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buildings'] = Building.objects.all()
        return context

class FacultyCreateView(AdminOrManagerMixin, CreateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'custom_admin/faculty_form.html'
    success_url = reverse_lazy('custom_admin:faculty_list')

class FacultyUpdateView(AdminOrManagerMixin, UpdateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'custom_admin/faculty_form.html'
    success_url = reverse_lazy('custom_admin:faculty_list')

class FacultyDeleteView(AdminOrManagerMixin, DeleteView):
    model = Faculty
    template_name = 'custom_admin/faculty_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:faculty_list')

# Этажи
class FloorListView(AdminOrManagerMixin, ListView):
    model = Floor
    template_name = 'custom_admin/floor_list.html'
    context_object_name = 'floors'
    paginate_by = 10

    def get_queryset(self):
        queryset = Floor.objects.all().select_related('building__university')
        building_id = self.request.GET.get('building')
        if building_id:
            queryset = queryset.filter(building_id=building_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buildings'] = Building.objects.all()
        return context

class FloorCreateView(AdminOrManagerMixin, CreateView):
    model = Floor
    form_class = FloorForm
    template_name = 'custom_admin/floor_form.html'
    success_url = reverse_lazy('custom_admin:floor_list')

class FloorUpdateView(AdminOrManagerMixin, UpdateView):
    model = Floor
    form_class = FloorForm
    template_name = 'custom_admin/floor_form.html'
    success_url = reverse_lazy('custom_admin:floor_list')

class FloorDeleteView(AdminOrManagerMixin, DeleteView):
    model = Floor
    template_name = 'custom_admin/floor_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:floor_list')

# Кабинеты
class RoomListView(AdminOrManagerMixin, ListView):
    model = Room
    template_name = 'custom_admin/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10

    def get_queryset(self):
        queryset = Room.objects.all().select_related('floor__building__university')
        university_id = self.request.GET.get('university')
        building_id = self.request.GET.get('building')
        floor_id = self.request.GET.get('floor')
        if university_id:
            queryset = queryset.filter(floor__building__university_id=university_id)
        if building_id:
            queryset = queryset.filter(floor__building_id=building_id)
        if floor_id:
            queryset = queryset.filter(floor_id=floor_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['universities'] = University.objects.all()
        context['buildings'] = Building.objects.all()
        context['floors'] = Floor.objects.all()
        return context

class RoomCreateView(AdminOrManagerMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'custom_admin/room_form.html'
    success_url = reverse_lazy('custom_admin:room_list')

class RoomUpdateView(AdminOrManagerMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'custom_admin/room_form.html'
    success_url = reverse_lazy('custom_admin:room_list')

class RoomDeleteView(AdminOrManagerMixin, DeleteView):
    model = Room
    template_name = 'custom_admin/room_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:room_list')

# Кафедры
class DepartmentListView(AdminOrManagerMixin, ListView):
    model = Department
    template_name = 'custom_admin/department_list.html'
    context_object_name = 'departments'
    paginate_by = 10

    def get_queryset(self):
        queryset = Department.objects.all().select_related('faculty__building__university')
        faculty_id = self.request.GET.get('faculty')
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faculties'] = Faculty.objects.all()
        return context

class DepartmentCreateView(AdminOrManagerMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'custom_admin/department_form.html'
    success_url = reverse_lazy('custom_admin:department_list')

class DepartmentUpdateView(AdminOrManagerMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'custom_admin/department_form.html'
    success_url = reverse_lazy('custom_admin:department_list')

class DepartmentDeleteView(AdminOrManagerMixin, DeleteView):
    model = Department
    template_name = 'custom_admin/department_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:department_list')

# Оборудование
class EquipmentListView(AdminOrManagerMixin, ListView):
    model = Equipment
    template_name = 'custom_admin/equipment_list.html'
    context_object_name = 'equipment'
    paginate_by = 10

    def get_queryset(self):
        queryset = Equipment.objects.all().select_related('type', 'room__floor__building__university', 'contract')
        room_id = self.request.GET.get('room')
        type_id = self.request.GET.get('type')
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        context['equipment_types'] = EquipmentType.objects.all()
        return context

class EquipmentCreateView(AdminOrManagerMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'custom_admin/equipment_form.html'
    success_url = reverse_lazy('custom_admin:equipment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(f"EquipmentCreateView: kwargs={kwargs}")
        return kwargs

    def form_valid(self, form):
        print(f"EquipmentCreateView: form valid, data={form.cleaned_data}")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f"EquipmentCreateView: form invalid, errors={form.errors}")
        return super().form_invalid(form)

class EquipmentUpdateView(AdminOrManagerMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'custom_admin/equipment_form.html'
    success_url = reverse_lazy('custom_admin:equipment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(f"EquipmentCreateView: kwargs={kwargs}")
        return kwargs

    def form_valid(self, form):
        print(f"EquipmentCreateView: form valid, data={form.cleaned_data}")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f"EquipmentCreateView: form invalid, errors={form.errors}")
        return super().form_invalid(form)

class EquipmentDeleteView(AdminOrManagerMixin, DeleteView):
    model = Equipment
    template_name = 'custom_admin/equipment_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:equipment_list')

# Договоры
class ContractDocumentListView(AdminOrManagerMixin, ListView):
    model = ContractDocument
    template_name = 'custom_admin/contract_document_list.html'
    context_object_name = 'contracts'
    paginate_by = 10

class ContractDocumentCreateView(AdminOrManagerMixin, CreateView):
    model = ContractDocument
    form_class = ContractDocumentForm
    template_name = 'custom_admin/contract_document_form.html'
    success_url = reverse_lazy('custom_admin:contract_document_list')

class ContractDocumentUpdateView(AdminOrManagerMixin, UpdateView):
    model = ContractDocument
    form_class = ContractDocumentForm
    template_name = 'custom_admin/contract_document_form.html'
    success_url = reverse_lazy('custom_admin:contract_document_list')

class ContractDocumentDeleteView(AdminOrManagerMixin, DeleteView):
    model = ContractDocument
    template_name = 'custom_admin/contract_document_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:contract_document_list')

# Пользователи
class UserListView(AdminOrManagerMixin, ListView):
    model = User
    template_name = 'custom_admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        return queryset

class UserCreateView(AdminOrManagerMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'custom_admin/user_form.html'
    success_url = reverse_lazy('custom_admin:user_list')

class UserUpdateView(AdminOrManagerMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'custom_admin/user_form.html'
    success_url = reverse_lazy('custom_admin:user_list')

class UserDeleteView(AdminOrManagerMixin, DeleteView):
    model = User
    template_name = 'custom_admin/user_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:user_list')

# Перемещения
class MovementListView(AdminOrManagerMixin, ListView):
    model = MovementHistory
    template_name = 'custom_admin/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 10

    def get_queryset(self):
        queryset = MovementHistory.objects.all().select_related('equipment', 'from_room', 'to_room')
        equipment_id = self.request.GET.get('equipment')
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = Equipment.objects.all()
        return context

class MovementCreateView(AdminOrManagerMixin, CreateView):
    model = MovementHistory
    form_class = MovementForm
    template_name = 'custom_admin/movement_form.html'
    success_url = reverse_lazy('custom_admin:movement_list')

class MovementUpdateView(AdminOrManagerMixin, UpdateView):
    model = MovementHistory
    form_class = MovementForm
    template_name = 'custom_admin/movement_form.html'
    success_url = reverse_lazy('custom_admin:movement_list')

class MovementDeleteView(AdminOrManagerMixin, DeleteView):
    model = MovementHistory
    template_name = 'custom_admin/movement_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:movement_list')


# Типы оборудования
class EquipmentTypeListView(AdminOrManagerMixin, ListView):
    model = EquipmentType
    template_name = 'custom_admin/equipment_type_list.html'
    context_object_name = 'equipment_types'
    paginate_by = 10

class EquipmentTypeCreateView(AdminOrManagerMixin, CreateView):
    model = EquipmentType
    form_class = EquipmentTypeForm
    template_name = 'custom_admin/equipment_type_form.html'
    success_url = reverse_lazy('custom_admin:equipment_type_list')

class EquipmentTypeUpdateView(AdminOrManagerMixin, UpdateView):
    model = EquipmentType
    form_class = EquipmentTypeForm
    template_name = 'custom_admin/equipment_type_form.html'
    success_url = reverse_lazy('custom_admin:equipment_type_list')

class EquipmentTypeDeleteView(AdminOrManagerMixin, DeleteView):
    model = EquipmentType
    template_name = 'custom_admin/equipment_type_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:equipment_type_list')