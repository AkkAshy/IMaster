# inventory/views.py (исправленная версия)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.core.exceptions import FieldError

# Импортируем модели напрямую
from .models import (
    PrinterChar, ExtenderChar, RouterChar, TVChar,
    NotebookChar, MonoblokChar, ProjectorChar, WhiteboardChar, MonitorChar,
    PrinterSpecification, ExtenderSpecification, RouterSpecification,
    TVSpecification, NotebookSpecification, MonoblokSpecification,
    ProjectorSpecification, WhiteboardSpecification, MonitorSpecification
)

# Импортируем сериализаторы
from .char_serializers import (
    PrinterCharSerializer, ExtenderCharSerializer, RouterCharSerializer,
    TVCharSerializer, NotebookCharSerializer, MonoblokCharSerializer,
    ProjectorCharSerializer, WhiteboardCharSerializer, MonitorCharSerializer,
    EquipmentSearchSerializer, EquipmentSearchResultSerializer
)

class EquipmentCharacteristicsViewSet(viewsets.ViewSet):
    """
    ViewSet для работы с характеристиками оборудования в inventory
    """
    permission_classes = [AllowAny]

    # Маппинг типов оборудования к моделям и сериализаторам
    EQUIPMENT_MAPPING = {
        'printer': {
            'model': PrinterChar,
            'serializer': PrinterCharSerializer,
            'specification_model': PrinterSpecification
        },
        'extender': {
            'model': ExtenderChar,
            'serializer': ExtenderCharSerializer,
            'specification_model': ExtenderSpecification
        },
        'router': {
            'model': RouterChar,
            'serializer': RouterCharSerializer,
            'specification_model': RouterSpecification
        },
        'tv': {
            'model': TVChar,
            'serializer': TVCharSerializer,
            'specification_model': TVSpecification
        },
        'notebook': {
            'model': NotebookChar,
            'serializer': NotebookCharSerializer,
            'specification_model': NotebookSpecification
        },
        'monoblok': {
            'model': MonoblokChar,
            'serializer': MonoblokCharSerializer,
            'specification_model': MonoblokSpecification
        },
        'projector': {
            'model': ProjectorChar,
            'serializer': ProjectorCharSerializer,
            'specification_model': ProjectorSpecification
        },
        'whiteboard': {
            'model': WhiteboardChar,
            'serializer': WhiteboardCharSerializer,
            'specification_model': WhiteboardSpecification
        }
    }

    @action(detail=False, methods=['get'])
    def list_all_characteristics(self, request):
        """
        Получить все характеристики всех типов оборудования
        """
        all_characteristics = {}

        for equipment_type, config in self.EQUIPMENT_MAPPING.items():
            try:
                model = config['model']
                serializer_class = config['serializer']

                # Проверяем, существует ли поле equipment в модели
                if hasattr(model, 'equipment'):
                    characteristics = model.objects.select_related('equipment').all()
                else:
                    characteristics = model.objects.all()

                # Добавляем связанные поля если они существуют
                if hasattr(model, 'specification'):
                    characteristics = characteristics.select_related('specification')
                if hasattr(model, 'author'):
                    characteristics = characteristics.select_related('author')

                serializer = serializer_class(characteristics, many=True, context={'request': request})

                all_characteristics[equipment_type] = {
                    'count': characteristics.count(),
                    'data': serializer.data
                }
            except Exception as e:
                all_characteristics[equipment_type] = {
                    'error': str(e),
                    'count': 0,
                    'data': []
                }

        return Response(all_characteristics)

    @action(detail=False, methods=['get'])
    def list_by_type(self, request):
        """
        Получить характеристики определенного типа оборудования
        """
        equipment_type = request.query_params.get('type')

        if not equipment_type or equipment_type not in self.EQUIPMENT_MAPPING:
            return Response(
                {
                    'error': 'Необходимо указать корректный тип оборудования',
                    'available_types': list(self.EQUIPMENT_MAPPING.keys())
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        config = self.EQUIPMENT_MAPPING[equipment_type]

        try:
            model = config['model']
            serializer_class = config['serializer']

            # Получаем базовый QuerySet
            if hasattr(model, 'equipment'):
                characteristics = model.objects.select_related('equipment')
            else:
                characteristics = model.objects.all()

            # Добавляем связанные поля если они существуют
            if hasattr(model, 'specification'):
                characteristics = characteristics.select_related('specification')
            if hasattr(model, 'author'):
                characteristics = characteristics.select_related('author')

            # Добавляем фильтрацию по параметрам
            filters = self._build_filters(request.query_params, equipment_type)
            if filters:
                characteristics = characteristics.filter(**filters)

            serializer = serializer_class(characteristics, many=True, context={'request': request})

            return Response({
                'type': equipment_type,
                'count': characteristics.count(),
                'data': serializer.data
            })

        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении данных: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def search_by_characteristic_id(self, request):
        """
        Поиск оборудования по ID конкретной характеристики
        Находит все оборудование с такими же характеристиками
        """
        equipment_type = request.query_params.get('type')
        characteristic_id = request.query_params.get('characteristic_id')

        if not equipment_type or not characteristic_id:
            return Response(
                {'error': 'Необходимо указать type и characteristic_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if equipment_type not in self.EQUIPMENT_MAPPING:
            return Response(
                {'error': 'Неподдерживаемый тип оборудования'},
                status=status.HTTP_400_BAD_REQUEST
            )

        config = self.EQUIPMENT_MAPPING[equipment_type]

        try:
            model = config['model']
            serializer_class = config['serializer']

            # Получаем исходную характеристику
            try:
                queryset = model.objects
                if hasattr(model, 'equipment'):
                    queryset = queryset.select_related('equipment')
                if hasattr(model, 'specification'):
                    queryset = queryset.select_related('specification')
                if hasattr(model, 'author'):
                    queryset = queryset.select_related('author')

                source_char = queryset.get(id=characteristic_id)
            except model.DoesNotExist:
                return Response(
                    {'error': f'Характеристика с ID {characteristic_id} не найдена'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Строим поисковые параметры на основе исходной характеристики
            search_params = self._extract_search_params_from_characteristic(source_char, equipment_type)

            # Ищем похожее оборудование (исключая исходное)
            similar_equipment = self._find_similar_equipment(
                model, search_params, exclude_id=characteristic_id
            )

            # Сериализуем результаты
            source_serializer = serializer_class(source_char, context={'request': request})
            similar_serializer = serializer_class(similar_equipment, many=True, context={'request': request})

            return Response({
                'equipment_type': equipment_type,
                'source_characteristic': {
                    'id': characteristic_id,
                    'data': source_serializer.data,
                    'search_params_used': search_params
                },
                'similar_equipment_count': similar_equipment.count(),
                'similar_equipment': similar_serializer.data,
                'search_summary': self._generate_search_summary(search_params, equipment_type)
            })

        except Exception as e:
            return Response(
                {'error': f'Ошибка поиска: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def get_characteristic_detail(self, request):
        """
        Получить детальную информацию о конкретной характеристике
        """
        equipment_type = request.query_params.get('type')
        characteristic_id = request.query_params.get('characteristic_id')

        if not equipment_type or not characteristic_id:
            return Response(
                {'error': 'Необходимо указать type и characteristic_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if equipment_type not in self.EQUIPMENT_MAPPING:
            return Response(
                {'error': 'Неподдерживаемый тип оборудования'},
                status=status.HTTP_400_BAD_REQUEST
            )

        config = self.EQUIPMENT_MAPPING[equipment_type]

        try:
            model = config['model']
            serializer_class = config['serializer']

            try:
                queryset = model.objects
                if hasattr(model, 'equipment'):
                    queryset = queryset.select_related('equipment')
                if hasattr(model, 'specification'):
                    queryset = queryset.select_related('specification')
                if hasattr(model, 'author'):
                    queryset = queryset.select_related('author')

                characteristic = queryset.get(id=characteristic_id)
            except model.DoesNotExist:
                return Response(
                    {'error': f'Характеристика с ID {characteristic_id} не найдена'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = serializer_class(characteristic, context={'request': request})

            # Добавляем дополнительную информацию
            response_data = serializer.data
            response_data['search_params'] = self._extract_search_params_from_characteristic(
                characteristic, equipment_type
            )

            return Response({
                'equipment_type': equipment_type,
                'characteristic_id': characteristic_id,
                'data': response_data
            })

        except Exception as e:
            return Response(
                {'error': f'Ошибка получения данных: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def available_types(self, request):
        """
        Получить список всех доступных типов оборудования
        """
        types_info = {}

        for equipment_type, config in self.EQUIPMENT_MAPPING.items():
            model = config['model']
            try:
                count = model.objects.count()
                types_info[equipment_type] = {
                    'name': equipment_type.title(),
                    'count': count,
                    'model_name': model.__name__
                }
            except Exception as e:
                types_info[equipment_type] = {
                    'name': equipment_type.title(),
                    'count': 0,
                    'model_name': model.__name__,
                    'error': str(e)
                }

        return Response({
            'available_types': types_info,
            'total_types': len(self.EQUIPMENT_MAPPING)
        })

    @action(detail=False, methods=['get'])
    def equipment_by_specification(self, request):
        """
        Найти все оборудование использующее определенную спецификацию
        """
        equipment_type = request.query_params.get('type')
        specification_id = request.query_params.get('specification_id')

        if not equipment_type or not specification_id:
            return Response(
                {'error': 'Необходимо указать type и specification_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if equipment_type not in self.EQUIPMENT_MAPPING:
            return Response(
                {'error': 'Неподдерживаемый тип оборудования'},
                status=status.HTTP_400_BAD_REQUEST
            )

        config = self.EQUIPMENT_MAPPING[equipment_type]

        try:
            model = config['model']
            serializer_class = config['serializer']

            # Проверяем есть ли поле specification
            if not hasattr(model, 'specification'):
                return Response(
                    {'error': f'Модель {equipment_type} не поддерживает спецификации'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Ищем оборудование с указанной спецификацией
            queryset = model.objects.filter(specification_id=specification_id)

            if hasattr(model, 'equipment'):
                queryset = queryset.select_related('equipment')
            if hasattr(model, 'specification'):
                queryset = queryset.select_related('specification')
            if hasattr(model, 'author'):
                queryset = queryset.select_related('author')

            serializer = serializer_class(queryset, many=True, context={'request': request})

            return Response({
                'equipment_type': equipment_type,
                'specification_id': specification_id,
                'equipment_count': queryset.count(),
                'equipment': serializer.data
            })

        except Exception as e:
            return Response(
                {'error': f'Ошибка поиска: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _extract_search_params_from_characteristic(self, characteristic, equipment_type):
        """
        Извлекает параметры поиска из объекта характеристики
        """
        search_params = {}

        # Определяем поля для каждого типа оборудования
        field_mappings = {
            'printer': ['model', 'serial_number', 'color', 'duplex'],
            'extender': ['ports', 'length'],
            'router': ['model', 'serial_number', 'ports', 'wifi_standart'],
            'tv': ['model', 'serial_number', 'screen_size'],
            'notebook': ['cpu', 'ram', 'monitor_size'],
            'monoblok': ['cpu', 'ram', 'monitor_size', 'has_keyboard', 'has_mouse'],
            'projector': ['model', 'lumens', 'resolution', 'throw_type'],
            'whiteboard': ['model', 'screen_size', 'touch_type'],
            'monitor': ['model', 'screen_size', 'resolution']
        }

        if equipment_type in field_mappings:
            for field in field_mappings[equipment_type]:
                if hasattr(characteristic, field):
                    value = getattr(characteristic, field)
                    if value is not None and value != '':
                        search_params[field] = value

        return search_params

    def _find_similar_equipment(self, model, search_params, exclude_id=None):
        """
        Ищет похожее оборудование по параметрам
        """
        # Строим Q объекты для гибкого поиска
        q_objects = Q()

        for field, value in search_params.items():
            if isinstance(value, bool):
                # Точное совпадение для булевых полей
                q_objects &= Q(**{field: value})
            elif isinstance(value, (int, float)):
                # Точное совпадение для числовых полей
                q_objects &= Q(**{field: value})
            else:
                # Частичное совпадение для текстовых полей
                q_objects &= Q(**{f'{field}__icontains': value})

        queryset = model.objects.filter(q_objects)

        # Добавляем связанные поля
        if hasattr(model, 'equipment'):
            queryset = queryset.select_related('equipment')
        if hasattr(model, 'specification'):
            queryset = queryset.select_related('specification')
        if hasattr(model, 'author'):
            queryset = queryset.select_related('author')

        # Исключаем исходную характеристику
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)

        return queryset

    def _generate_search_summary(self, search_params, equipment_type):
        """
        Генерирует краткое описание параметров поиска
        """
        if not search_params:
            return "Поиск без параметров"

        summary_parts = []

        # Человекочитаемые названия полей
        field_names = {
            'model': 'Модель',
            'serial_number': 'Серийный номер',
            'color': 'Цветной',
            'duplex': 'Дуплекс',
            'ports': 'Порты',
            'length': 'Длина',
            'wifi_standart': 'Wi-Fi стандарт',
            'screen_size': 'Размер экрана',
            'cpu': 'Процессор',
            'ram': 'Оперативная память',
            'monitor_size': 'Размер монитора',
            'has_keyboard': 'Клавиатура',
            'has_mouse': 'Мышь',
            'lumens': 'Яркость',
            'resolution': 'Разрешение',
            'throw_type': 'Тип проекции',
            'touch_type': 'Тип сенсора'
        }

        for field, value in search_params.items():
            field_name = field_names.get(field, field)

            if isinstance(value, bool):
                value_str = 'Да' if value else 'Нет'
            else:
                value_str = str(value)

            summary_parts.append(f"{field_name}: {value_str}")

        return f"Поиск по: {'; '.join(summary_parts)}"

    def _build_filters(self, query_params, equipment_type):
        """
        Построение фильтров на основе параметров запроса
        """
        filters = {}

        # Общие поля
        common_fields = ['model', 'serial_number']

        # Специфичные поля для каждого типа
        type_specific_fields = {
            'printer': ['color', 'duplex'],
            'extender': ['ports', 'length'],
            'router': ['ports', 'wifi_standart'],
            'tv': ['screen_size'],
            'notebook': ['cpu', 'ram', 'monitor_size'],
            'monoblok': ['cpu', 'ram', 'monitor_size', 'has_keyboard', 'has_mouse'],
            'projector': ['lumens', 'resolution', 'throw_type'],
            'whiteboard': ['screen_size', 'touch_type'],
            'monitor': ['screen_size', 'resolution']
        }

        # Добавляем общие фильтры
        for field in common_fields:
            value = query_params.get(field)
            if value:
                filters[f'{field}__icontains'] = value

        # Добавляем специфичные фильтры
        if equipment_type in type_specific_fields:
            for field in type_specific_fields[equipment_type]:
                value = query_params.get(field)
                if value is not None:
                    if field in ['color', 'duplex', 'has_keyboard', 'has_mouse']:
                        # Булевы поля
                        filters[field] = value.lower() in ['true', '1', 'yes']
                    elif field in ['ports', 'lumens']:
                        # Числовые поля
                        try:
                            filters[field] = int(value)
                        except ValueError:
                            pass
                    else:
                        # Текстовые поля
                        filters[f'{field}__icontains'] = value

        return filters