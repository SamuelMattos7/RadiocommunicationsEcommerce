import django_filters
from django.db import models
from .models import Producto, TipoProductos, CodigosProductos

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label='Search')
    precio_min = django_filters.NumberFilter(field_name='Precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='Precio', lookup_expr='lte')
    tipo = django_filters.ModelChoiceFilter(queryset=TipoProductos.objects.all(), field_name='Tipo')
    codigo = django_filters.ModelChoiceFilter(queryset = CodigosProductos.objects.all(), field_name='Codigos')

    class Meta: 
        model = Producto
        fields = ['precio_min', 'precio_max', 'tipo', 'codigo']

    def filter_by_all(self, queryset, name, value):

        return queryset.filter(
            models.Q(Nombre__icontains=value) | models.Q(Marca__icontains=value)
        )